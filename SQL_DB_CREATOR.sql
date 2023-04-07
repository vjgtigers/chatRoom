CREATE SCHEMA vjgtigers_chatroom;
CREATE TABLE vjgtigers_chatroom.login_data (
    login_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    client_id int UNIQUE,
    email VARCHAR(45),
    password VARCHAR(200)
);
CREATE TABLE vjgtigers_chatroom.banned_ips (
	banned_ip int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    ipaddress VARCHAR(45)
);
CREATE TABLE vjgtigers_chatroom.client_room (
	client_id int,
    room_id int,
	client_room_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT
);
CREATE TABLE vjgtigers_chatroom.clients (
	client_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(45),
    active int
);
CREATE TABLE vjgtigers_chatroom.history (
	history_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    room_id int,
    client_id int,
    message1 LONGTEXT,
    time_date VARCHAR(45)
    

);
CREATE TABLE vjgtigers_chatroom.rooms (
	room_id int NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(45)
);