/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - cryptography
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`cryptography` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cryptography`;

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaintid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `complaintdate` date DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `replydate` date DEFAULT NULL,
  PRIMARY KEY (`complaintid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin@gmail.com','admin','admin'),(18,'rukiyathsaifunisah@gmail.com','s','user'),(20,'rameesyounus49@gmail.com','r','user'),(23,'salmaaslam977@gmail.com','sa','user'),(24,'shebipc13@gmail.com','F','user'),(27,'salmaaslam977@lbscek.ac.in','salma','user'),(28,'salmaaslam977@lbscek.ac.in','salma123','user');

/*Table structure for table `upload` */

DROP TABLE IF EXISTS `upload`;

CREATE TABLE `upload` (
  `fileid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  `uploaddate` date DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `no_of_page` varchar(50) DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  `path` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`fileid`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

/*Data for the table `upload` */

insert  into `upload`(`fileid`,`userid`,`file`,`uploaddate`,`type`,`no_of_page`,`filename`,`path`) values (29,27,'/static/server1/20220606_144522.png','2022-06-06','image','1','eg1','/static/orgg/20220606_144522.png');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `uloginid` int(11) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `Phoneno` bigint(10) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`uloginid`,`username`,`email`,`Phoneno`,`image`) values (18,'saifu23','rukiyathsaifunisah@gmail.com',6282369030,NULL),(20,'ramees','rameesyounus49@gmail.com',9061110291,NULL),(23,'SALMA','salmaaslam977@gmail.com',9895606977,NULL),(24,'Shabida Shebeen P C','shebipc13@gmail.com',7558854278,NULL),(27,'salma','salmaaslam977@lbscek.ac.in',9895606977,'/static/user_imgs/20220606_144241.jpg'),(28,'salma','salmaaslam977@lbscek.ac.in',9895606977,'/static/user_imgs/20220606_144246.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
