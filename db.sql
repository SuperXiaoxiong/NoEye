create  database noeye default charset utf8;
use noeye;

/* query from url*/
create table dns_query(
 id int unsigned not null AUTO_INCREMENT, 
 prefixdata text,
 lastaccess TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(`id`),
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;
 
 create table  url_query(
 id int unsigned not null AUTO_INCREMENT,
 queried_key  varchar(64),
 lastaccess   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,/* key access time*/
 PRIMARY KEY(`id`)
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;
