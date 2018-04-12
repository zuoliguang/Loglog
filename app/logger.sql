
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(10) unsigned NOT NULL COMMENT '用户id',
  `method` varchar(5) NOT NULL COMMENT '请求方式 GET,POST,PUT,DELETE...',
  `header` varchar(600) NOT NULL COMMENT '请求头信息',
  `query` varchar(225) DEFAULT NULL COMMENT '参数信息',
  `date` varchar(10) NOT NULL COMMENT '日期',
  `time` varchar(8) DEFAULT NULL COMMENT '时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;