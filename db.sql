create table database noeye default charset utf8;
use noeye;

/* query from url*/
create table dns_query(
 id int unsigned not null AUTO_INCREMENT, 
 prefixdata text,
 lastaccess TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 user_key varchar(64),
 PRIMARY KEY(`id`),
 KEY `idx_user_key` (`user_key`)
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;
 
 create table  url_query(
 id int unsigned not null AUTO_INCREMENT,
 queried_key  varchar(64),
 lastaccess   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP/* key access time*/
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;
