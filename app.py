#!/usr/bin/env python
from flask import Flask, render_template, Response, url_for, request, redirect, session, jsonify
from datetime import date
import cv2
import pymysql
import os


faceCascade=cv2.CascadeClassifier("static/haarcascade_frontalface_default.xml")
today = date.today()
app = Flask(__name__)
video = cv2.VideoCapture(0)
conn=pymysql.connect('localhost','project_python','jFgIgOef04v83vZ3','dbpython',charset='utf8')

def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,clf):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    features=classifier.detectMultiScale(gray,scaleFactor,minNeighbors,minSize=(55, 55))
    coords=[]
    for (x,y,w,h) in features:
        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
        id,con= clf.predict(gray[y:y+h,x:x+w])
        names="59042380"+str(id)
        cons = " {0}%".format(round(100 - con))
        credibility = " {0}".format(round(100 - con))
        sid = str(names)
        currentDate = today.strftime("%Y-%m-%d")
        if con <= 40 :
            cv2.putText(img,str(names),(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
            cur=conn.cursor()
            cur.execute("SELECT * FROM timestamps WHERE sid = %s AND ts_date = %s",(sid,currentDate))
            rows=cur.fetchone()
            if not rows :
                imgstamp = currentDate+'-'+str(names)+'.jpg'
                sql="INSERT INTO `timestamps` (`sid`,`ts_credibility`,`ts_img`) VALUES(%s,%s,%s)"
                cur.execute(sql,(sid,credibility,imgstamp))
                conn.commit()
                cv2.imwrite('static/imgstamp/'+imgstamp+'.jpg', img)
        coords=[x,y,w,h]
    return img,coords

def create_dataset(img,id,img_id):
        cv2.imwrite("static/imgdataset/img."+str(id)+"."+str(img_id)+".jpg",img)

def draw_boundaryRC(img,classifier,scaleFactor,minNeighbors,color,text):
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        features=classifier.detectMultiScale(gray,scaleFactor,minNeighbors,minSize=(55, 55))
        coords=[]
        for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
                coords=[x,y,w,h]
        return img,coords

def detect(img,faceCascade,img_id,clf):
    img,coords=draw_boundary(img,faceCascade,1.1,10,(0,0,255),clf)
    if len(coords)==4 :
        result = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
    return img

def detectRC(img,faceCascade,img_ids):
    img,coords=draw_boundaryRC(img,faceCascade,1.1,10,(0,0,255),"Face")
    if len(coords)==4 :
            result = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
            create_dataset(result,'136',img_ids)
    return img

def gen():
    img_id=0
    clf=cv2.face.LBPHFaceRecognizer_create()
    clf.read("static/classifier.xml")
    while True:
        rval, frame = video.read()
        frame=detect(frame,faceCascade,img_id,clf)
        cv2.imwrite('t.jpg', frame)
        img_id+=1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

def refreshRecognized():
    return render_template('recognized.html')

def genRC():
    img_ids=0
    while (True):
            ret,frame = video.read()
            frame=detectRC(frame,faceCascade,img_ids)
            cv2.imwrite('f.jpg', frame)
            img_ids+=1
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('f.jpg', 'rb').read() + b'\r\n')
            if img_ids==100:
                refreshRecognized()
                break

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create_students')
def create_students():
    session.clear()
    with conn:
        cur=conn.cursor()
        cur.execute("SELECT * FROM students")
        rows=cur.fetchall()
        return render_template('create_students.html',datas=rows)

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    with conn:
        cur=conn.cursor()
        cur.execute("DELETE FROM students where id=%s", (id_data))
        rows=cur.fetchall()
        return redirect(url_for('create_students'))

@app.route('/insert_students',methods=['POST'])
def insert_students():
    session.clear()
    if request.method=="POST":
        id=request.form['ids']
        pname=request.form['pname']
        fname=request.form['fname']
        lname=request.form['lname']
        with conn.cursor() as cursor:
            sql="INSERT INTO `students` (`id`,`pname`,`fname`,`lname`) VALUES(%s,%s,%s,%s)"
            try:
                cursor.execute(sql,(id,pname,fname,lname))
                conn.commit()
                session['stsuccess'] = 'เพิ่มข้อมูล เรียบร้อยแล้ว'
            except:
                conn.rollback()
                session['stfail'] = 'เพิ่มข้อมูล ผิดพลาด'
    return redirect(url_for('create_students'))

@app.route('/detect_report')
def detect_report():
    if request.args.get('monthh',type = int) :
        m = request.args.get('monthh',type = int)
    else :
        m = int(today.strftime("%m"))
    showmonths = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
    mName = showmonths[m-1]
    cur=conn.cursor()
    cur.execute("SELECT timestamps.* , students.pname , students.fname , students.lname  FROM timestamps INNER JOIN students ON timestamps.sid=students.id WHERE MONTH(timestamps.ts_date) = %s",(m))
    rows=cur.fetchall()
    return render_template('detect_report.html',showmonths=showmonths,monthh=mName,datas=rows)

@app.route('/detect_info')
def detect_info():
    ts_id = request.args.get('id',type = int)
    cur=conn.cursor()
    cur.execute("SELECT timestamps.* , students.pname , students.fname , students.lname  FROM timestamps INNER JOIN students ON timestamps.sid=students.id WHERE timestamps.ts_id = %s",(ts_id))
    rows=cur.fetchone()
    return render_template('detect_info.html',rows=rows)

@app.route('/iframe_query')
def iframe_query():
    currentDate = today.strftime("%Y-%m-%d")
    with conn:
        cur=conn.cursor()
        cur.execute("SELECT timestamps.* , students.pname , students.fname , students.lname  FROM timestamps INNER JOIN students ON timestamps.sid=students.id WHERE timestamps.ts_date = %s",(currentDate))
        rows=cur.fetchall()
        return render_template('iframe_query.html',datas=rows)

@app.route('/recognized')
def recognized():
    return render_template('recognized.html')


@app.route('/video_recognize')
def video_recognize():
    return Response(genRC(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='127.0.0.1', port='0136', debug=True, threaded=True)
