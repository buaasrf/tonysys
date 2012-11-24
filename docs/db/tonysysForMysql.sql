-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.25 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-11-18 12:40:02
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping database structure for tonysys
DROP DATABASE IF EXISTS `DB_TONYSYS`;
CREATE DATABASE IF NOT EXISTS `DB_TONYSYS` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `DB_TONYSYS`;


-- Dumping structure for table tonysys.conduct_score
DROP TABLE IF EXISTS `conduct_score`;
CREATE TABLE IF NOT EXISTS `conduct_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(16) DEFAULT NULL COMMENT '操行类别,出操/内务/考勤',
  `number` varchar(16) NOT NULL COMMENT '学号/工号',
  `name` varchar(16) DEFAULT NULL COMMENT '姓名',
  `grade` varchar(16) DEFAULT NULL COMMENT '班级',
  `score` tinyint(4) DEFAULT NULL COMMENT '分数',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '日期时间',
  `place` varchar(32) DEFAULT NULL COMMENT '地点',
  `remark` varchar(32) DEFAULT NULL COMMENT '备注',
  `description` varchar(64) DEFAULT NULL COMMENT '描述',
  `updateBy` varchar(16) DEFAULT NULL,
  `updateDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `createBy` varchar(16) DEFAULT NULL,
  `createDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='操行分对象';

-- Data exporting was unselected.


-- Dumping structure for table tonysys.dormitory
DROP TABLE IF EXISTS `dormitory`;
CREATE TABLE IF NOT EXISTS `dormitory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `building` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `room` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `door` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bednumber` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='宿舍信息表';

-- Data exporting was unselected.


-- Dumping structure for table tonysys.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(16) DEFAULT NULL COMMENT '用户类别（不同权限）student, 军体部长,劳生部长,纪检部长, teacher, admin, root',
  `number` varchar(16) NOT NULL COMMENT '学号/工号',
  `password` varchar(32) DEFAULT NULL COMMENT '密码',
  `name` varchar(16) DEFAULT NULL COMMENT '姓名',
  `dept` varchar(16) DEFAULT NULL COMMENT '院(系)/部',
  `trainingLevel` varchar(16) DEFAULT NULL COMMENT '培养层次',
  `subject` varchar(16) DEFAULT NULL COMMENT '专业',
  `grade` varchar(16) DEFAULT NULL COMMENT '班级',
  `state` varchar(16) DEFAULT NULL COMMENT '状态',
  `gender` varchar(16) DEFAULT NULL COMMENT '性别',
  `nation` varchar(16) DEFAULT NULL COMMENT '民族',
  `province` varchar(16) DEFAULT NULL COMMENT '籍贯',
  `birth` varchar(16) DEFAULT NULL COMMENT '出生日期',
  `idNumber` varchar(32) DEFAULT NULL COMMENT '身份证号',
  `candidateNumber` varchar(16) DEFAULT NULL COMMENT '考生号',
  `examNumber` varchar(16) DEFAULT NULL COMMENT '准考证号',
  `politicsStatus` varchar(16) DEFAULT NULL COMMENT '政治面貌',
  `email` varchar(32) DEFAULT NULL COMMENT '电子邮箱',
  `phone` varchar(16) DEFAULT NULL COMMENT '联系电话',
  `homePhone` varchar(16) DEFAULT NULL COMMENT '家庭电话',
  `remark` varchar(32) DEFAULT NULL COMMENT '备注',
  `fatherName` varchar(16) DEFAULT NULL COMMENT '父亲姓名',
  `fatherPhone` varchar(16) DEFAULT NULL COMMENT '联系电话',
  `motherName` varchar(16) DEFAULT NULL COMMENT '母亲姓名',
  `motherPhone` varchar(16) DEFAULT NULL COMMENT '联系电话',
  `descrition` varchar(64) DEFAULT NULL COMMENT '描述',
  `updateBy` varchar(16) DEFAULT NULL,
  `updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `createBy` varchar(16) DEFAULT NULL,
  `createDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dormitoryid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `FK_user_dormitory` (`dormitoryid`),
  CONSTRAINT `FK_user_dormitory` FOREIGN KEY (`dormitoryid`) REFERENCES `dormitory` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户对象';

-- Data exporting was unselected.
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
