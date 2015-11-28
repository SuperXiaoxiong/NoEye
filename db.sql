/*
NoeYe just for fun.
author:KibodWapon
blog:http://www.163.com/cmdbat@126
*/
create table database noeye default charset utf8;
grant all on noeye.* to noeyeuser@'loccalhost' identified by 'noeye_n033y3_';
use noeye;

/* query from url*/
create table dns_querys(
 id int unsigned, 
 a text,/* a record*/
 user_key varchar(64),/*user key ,second layer domain */
 KEY `idx_user_key` (`user_key`)
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;;
 
 create table  url_query(
 id int unsigned,
 queried_key  varchar(64),
 lastaccess   datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP/* key access time*/
 )ENGINE=MyISAM  DEFAULT CHARSET=utf8;;
