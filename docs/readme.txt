

系统基于Windows + Tomcat + Mysql 平台，采用javaEE技术（struts2 + jsp + dbutils）。
控制层由struts2提供控制流程，业务逻辑和数据访问由dbutils+javaBean实现。
表现层采用Ajax,JSP与JSTL及EL相结合。

一：
1. jdk安装与配置与Eclipse安装：
配置JAVA_HOME

2. Mysql数据库安装与访问， 表结构见docs/db/tonysysForMysql.sql ： 
配置MYSQL_HOME与启动服务 
mysql -h localhost -u root -D tonysys
select * from user;
select * from conduct_score;

3. tomcat安装见，与tony sys应用部署：（参考资料http://wenku.baidu.com/view/46c77c8002d276a200292ef0.html）
压缩版tomcat，配置CATALINA_HOME
部署服务：
   apache-tomcat-7.0.6\webapps\下 新建目录tonysys
   tonysys\WebRoot目录的所有文件 复制到 tonysys目录下。
启动tomcat：apache-tomcat-7.0.6\bin>catalina.bat start
停止tomcat：apache-tomcat-7.0.6\bin>catalina.bat stop


二： 
Tony Sys Manager构建在本机调试环境配置列表：
url： http://127.0.0.1:8080/tonysys/
用户密码：root/abc

1. log4j修改：
src\log4j.properties中
如果需调试信息：log4j.rootLogger修改为DEBUG, CONSOLE, DAILY_ROLLING_FILE；
如：log4j.rootLogger=DEBUG, CONSOLE, DAILY_ROLLING_FILE

如需调试信息且记录到文件中：
log4j.appender.DAILY_ROLLING_FILE.Threshold修改为ERROR；
如：log4j.appender.DAILY_ROLLING_FILE.Threshold=DEBUG

log4j.appender.DAILY_ROLLING_FILE.File修改为本机日志存放路径文件；
如：log4j.appender.DAILY_ROLLING_FILE.File=../logs/tonysys.log

2. src\com\tony\sys\config
数据库参数配置：db.properties
业务层配置：biz.properties
持久层配置：dao.properties

3. src\struts.xml
struts2配置

