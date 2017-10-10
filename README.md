# NoEye

## update 2017-10-10:

### 实用场景：
	data:子域:域名
	单用户版，不再需要user_key,自行搭建的dns，http隐蔽通道
	可以设置htaccess 对查询数据页面进行保护

### 使用方法：
	1. 在mysql中使用db.sql创建对应数据库和表，数据库名称noeye
	2. 修改NoEye.py响应的domainname ，subdomain和数据库连接相关信息
	3. sudo python NoEye.py //需要sudo权限，只将收集数据存储在dns_query表中
	4. 访问noeye.php查看 dns和http获取的数据
	5. dig data.subdomain.domainname  //传输dns data
	6. http_noeye.php?data=data   //传输http data

## update 2016-03-16:

修复之前的程序错误:

  - db.sql与程序逻辑对不上

  - noeye.php 66行 mysql_real_escape_string修改成addslashes函数对输入数据处理。

##How to use?
> http://localhost/noeye.php?uk=md5(userkey)

Original readme:
	
	A blind exploit tool( a dns server and a web app) that like wvs's AcuMonitor Service or burpsuite's collabrator or cloudeye!

	Send me any bug to cmdbat#126.com
