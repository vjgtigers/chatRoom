CREATE SCHEMA vjgtigers_chatroom;
CREATE TABLE chatroom.login_data (
    login_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    client_id int UNIQUE,
    email VARCHAR(45),
    password VARCHAR(200)
);
CREATE TABLE chatroom.banned_ips (
	banned_ip int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    ipaddress VARCHAR(45)
);
CREATE TABLE chatroom.client_room (
	client_id int,
    room_id int,
	client_room_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT
);
CREATE TABLE chatroom.clients (
	client_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(45),
    active int
);
CREATE TABLE chatroom.history (
	history_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    room_id int,
    client_id int,
    message1 LONGTEXT,
    time_date VARCHAR(45)
    

);
CREATE TABLE chatroom.rooms (
	room_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(45)
);

CREATE TABLE chatroom.rooms (
	room_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(45)
);

CREATE TABLE chatroom.ip_logs (
	ipLogs_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    client_id int,
    ip_add VARCHAR(100),
    time_date VARCHAR(45)
    

);