#MySQL Schema

CREATE DATABASE IF NOT EXISTS kurgan;

USE kurgan;

CREATE TABLE IF NOT EXISTS users(
	id 		SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	login 		VARCHAR(255) NOT NULL,
	pass		VARCHAR(64) NOT NULL,
	email		VARCHAR(255) NOT NULL,
	level		ENUM('admin','operator','viewer'),
	enabled		BIT(1) DEFAULT 0
);

#default User

INSERT INTO users VALUES(1,"admin",SHA1("admin"),"admin@vortexai.com.br",NULL,NULL,"admin",1);


#Table for last ip, last time login;

CREATE TABLE IF NOT EXISTS last_login(
        id              SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        idlogin		SMALLINT NOT NULL,
        last_login      DATETIME,
        last_ip         VARCHAR(255) NOT NULL,
	user_agent	VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS last_scan(
        id              	SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        idlogin         	SMALLINT NOT NULL,
        time_executed   	DATETIME,
        url	                VARCHAR(255) NOT NULL,
        agent_output      	VARCHAR(255) NULL
);

