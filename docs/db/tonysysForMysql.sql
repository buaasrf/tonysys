

/*
--drop table user;
DROP DATABASE tonysys;
*/

CREATE DATABASE tonysys CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';
USE tonysys;

drop table user;
drop table conduct_score;

create table user (
	id INTEGER(11) NOT NULL AUTO_INCREMENT,
	type VARCHAR(16) COMMENT '用户类别（不同权限）student, 军体部长,劳生部长,纪检部长, teacher, admin, root',
	number VARCHAR(16) NOT NULL COMMENT '学号/工号',
	password VARCHAR(32) COMMENT '密码',
	name VARCHAR(16)  COMMENT '姓名',
	dept VARCHAR(16) COMMENT '院(系)/部',
	trainingLevel VARCHAR(16) COMMENT '培养层次',
	subject VARCHAR(16) COMMENT '专业',
	grade VARCHAR(16) COMMENT '班级',
	state VARCHAR(16) COMMENT '状态',    
	gender VARCHAR(16) COMMENT '性别',
	nation VARCHAR(16) COMMENT '民族',
	province VARCHAR(16) COMMENT '籍贯',
	birth VARCHAR(16) COMMENT '出生日期',    
	idNumber VARCHAR(32) COMMENT '身份证号', 
	candidateNumber VARCHAR(16) COMMENT '考生号',
	examNumber VARCHAR(16) COMMENT '准考证号', 
	politicsStatus VARCHAR(16) COMMENT '政治面貌',
	email VARCHAR(32) COMMENT '电子邮箱',  
	phone VARCHAR(16) COMMENT '联系电话',
	homePhone VARCHAR(16) COMMENT '家庭电话', 
	remark VARCHAR(32) COMMENT '备注',
	fatherName VARCHAR(16) COMMENT '父亲姓名',
	fatherPhone VARCHAR(16) COMMENT '联系电话',
	motherName VARCHAR(16) COMMENT '母亲姓名',
	motherPhone VARCHAR(16) COMMENT '联系电话',
	descrition VARCHAR(64) COMMENT '描述',
	updateBy VARCHAR(16),
	updateDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	createBy VARCHAR(16),
	createDate TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	UNIQUE KEY (number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户对象';
create table conduct_score (
	id INTEGER(11) NOT NULL AUTO_INCREMENT,
	type VARCHAR(16) COMMENT '操行类别,出操/内务/考勤',
	number VARCHAR(16) NOT NULL COMMENT '学号/工号',
	name VARCHAR(16)  COMMENT '姓名',
	grade VARCHAR(16) COMMENT '班级',
	score TINYINT(4)  COMMENT '分数',
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '日期时间',
    place VARCHAR(32)  COMMENT '地点',
	remark VARCHAR(32) COMMENT '备注',
	descrition VARCHAR(64) COMMENT '描述',
	updateBy VARCHAR(16),
	updateDate TIMESTAMP NOT NULL,
	createBy VARCHAR(16),
	createDate TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	UNIQUE KEY (number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='操行分对象';


/*
insert into user(, descrition, createBy, createDate) values(, 'userDesc0', 'yangwm0', '2010-03-20 12:30:44.515');
commit;
*/
