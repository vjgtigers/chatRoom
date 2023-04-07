<h1>This is currenly a python based server/client chatroom</h1><br>
<br>
<h3>Functionalitys currently include:</h3><br>
<br>
-diffrent roooms <br>
-login with email and password <br>
-username not email <br>
-sql database <br>
  -history table <br>
  -client/room info <br>
  -login <br>
  -userinfo <br>
  -bannedips <br>
-ability to create accounts <br>
-ability to bann ips <br>
<br>
<h3>Looking to add:</h3><br>
-account banning <br>
-spam protection <br>


<br><br><br>

<h3>Non server related things that i want to add</h3> <br>
 -execualtable client side (proabably in c++)<br>

<br><br>


<h2>Setup<h2><br>
<p>To run server first create a config.secret file. inside this file use the following format. (NOTHING in quotations)</p>
<br><br>
[server]<br>
<br>
db_ip = YOUR_DB_IP<br>
db_user = DB_USER<br>
db_password = DB_PASSWORD<br>
db_db = SCHEMA_NAME<br>
<br>
<h1>SQL Server Setup</h1>

<h4>A script now exists to do this for you called "SQL_DB_CREATOR.sql"</h4>

create a schemea<br>
banned_ips<br>
	-banned_id [INT] (PK,NN,UQ,AI)<br>
	-ipaddress [VARCHAR(45)]<br>
client_room<br>
	-client_room_id [INT] (PK,NN,UQ,AI)<br>
	-client_id [INT] <br>
	-room_id [INT] <br>
clients<br>
	client_id [INT] (PK,NN,UQ,AI)<br>
	nickname [VARCHAR(45)]<br>
	active [INT] <br>
history<br>
	-history_id [INT] (PK,NN,UQ,AI)<br>
	-room_id [INT] <br>
	-client_id [INT] <br>
	-message1 [LONGTEXT]<br>
	-time_data [VARCHAR(45)]<br>
login_data<br>
	-login_id [INT] (PK,NN,UQ,AI)<br>
	-client_id [INT] (UQ)<br>
	-email [VARCHAR(45)]<br>
	-password [VARCHAR(200)]<br>
rooms<br>
	-room_id [INT] (PK,NN,UQ,AI)<br>
	-room_name [VARCHAR(45)]<br>