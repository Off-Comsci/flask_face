-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.6-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for dbpython
CREATE DATABASE IF NOT EXISTS `dbpython` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `dbpython`;

-- Dumping structure for table dbpython.students
CREATE TABLE IF NOT EXISTS `students` (
  `id` char(11) COLLATE utf8_unicode_ci NOT NULL,
  `pname` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fname` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lname` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='ข้อมูลนักศึกษา';

-- Data exporting was unselected.

-- Dumping structure for table dbpython.timestamps
CREATE TABLE IF NOT EXISTS `timestamps` (
  `ts_id` int(11) NOT NULL AUTO_INCREMENT,
  `ts_date` date DEFAULT current_timestamp(),
  `sid` char(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ts_credibility` float(6,2) DEFAULT 0.00 COMMENT 'ความน่าเชื่อถือ ...%',
  `ts_time` time DEFAULT current_timestamp(),
  `ts_img` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ts_id`),
  UNIQUE KEY `ct_date` (`ts_date`,`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='เวลาเข้าเรียน';

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
