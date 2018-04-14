/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50547
Source Host           : localhost:3306
Source Database       : logger

Target Server Type    : MYSQL
Target Server Version : 50547
File Encoding         : 65001

Date: 2018-04-13 17:38:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admin`
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL COMMENT '账号',
  `password` varchar(100) NOT NULL DEFAULT 'e10adc3949ba59abbe56e057f20f883e' COMMENT '密码 md5 默认 123456',
  `type` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '管理账号类型 0超级 1普通',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'admin', 'e10adc3949ba59abbe56e057f20f883e', '0');

-- ----------------------------
-- Table structure for `log`
-- ----------------------------
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(15) NOT NULL,
  `method` varchar(10) NOT NULL,
  `route` varchar(30) NOT NULL,
  `header` varchar(255) NOT NULL,
  `query` varchar(255) NOT NULL,
  `date` varchar(10) NOT NULL,
  `time` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `全文搜索` (`uid`,`method`,`route`,`header`,`query`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of log
-- ----------------------------
INSERT INTO `log` VALUES ('1', '123', 'GET', '/study', 'header', 'k=v', '2015-04-23', '00:11:33');
INSERT INTO `log` VALUES ('2', '134', 'POST', '/user', 'header xxx', 'l=p', '2018-04-25', '11:22:44');
INSERT INTO `log` VALUES ('3', '198', 'GET', '/test', 'header yyy', 'x=y', '2017-04-19', '22:33:11');
INSERT INTO `log` VALUES ('4', '999', 'PUT', '/del', 'hearder', 'p=0', '2018-06-01', '23:55:44');
INSERT INTO `log` VALUES ('5', '666', 'GET', '/zlgcg', 'header', 'g=9', '2016-09-12', '19:33:30');
INSERT INTO `log` VALUES ('6', '888', 'POST', '/git', 'header', 'k=v', '2018-05-18', '23:11:33');
INSERT INTO `log` VALUES ('7', '999', 'GET', '/study', 'header', 'k=k', '2018-09-08', '18:13:14');
INSERT INTO `log` VALUES ('8', '3', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:29:04');
INSERT INTO `log` VALUES ('9', '2', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:29:04');
INSERT INTO `log` VALUES ('10', '1', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:29:04');
INSERT INTO `log` VALUES ('11', '0', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:29:04');
INSERT INTO `log` VALUES ('12', '4', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:22:09');
INSERT INTO `log` VALUES ('13', '3', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:22:09');
INSERT INTO `log` VALUES ('14', '2', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:22:09');
INSERT INTO `log` VALUES ('15', '1', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:22:09');
INSERT INTO `log` VALUES ('16', '0', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:22:09');
INSERT INTO `log` VALUES ('17', '2', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:21:08');
INSERT INTO `log` VALUES ('18', '1', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:21:08');
INSERT INTO `log` VALUES ('19', '0', 'POST', '/test', 'header', 'name=zlgcg', '2018-04-13', '17:21:08');
