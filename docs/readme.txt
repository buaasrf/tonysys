

系统基于jdk1.7平台，采用javaEE技术（springMVC）。
使用git作为代码版本控制工具。
使用maven进行系统构建

表现页面采用Ajax,JSP与JSTL及EL相结合。

一：
1. jdk1.7安装与配置:
下载安装jdk1.7
配置JAVA_HOME

2. Mysql数据库安装与访问， 表结构见docs/db/tonysysForMysql.sql ： 
配置MYSQL_HOME与启动服务 
mysql -h localhost -u root p root -D db_tonysys
select * from user;
select * from conduct_score;

3. tomcat安装见，与tonysys应用部署：（参考资料http://wenku.baidu.com/view/46c77c8002d276a200292ef0.html）
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

1. slf4j日志配置修改：
src\main\resource\tonysyslog.xml中

<appender name="tonysys_appender" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <File>${dauth.log.dir}/ad_visit.log</File>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <FileNamePattern>${dauth.log.dir}/ad_visit.%d{yyyy-MM-dd}.log</FileNamePattern>
        </rollingPolicy>

        <layout class="ch.qos.logback.classic.PatternLayout">
            <Pattern>%logger %d{yyyy-MM-dd HH:mm:ss} %msg%n</Pattern>
        </layout>
    </appender>

    <logger name="tonysys" class="com.tonysys.admin.*.*" level="debug">
        <appender-ref ref="tonysys_appender" />
    </logger>

2. src\main\filters\filter-*.properties
(注：其中*为：dev、product、test,分别表示三种运行状态，运行状态在pom.xml 中<project.environment>修改)
数据名称：db_instance_ad
用户名：db_username_ad
密码：db_password_ad


