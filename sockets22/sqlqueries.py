#import mysql.connector
import time
import datetime
import os
import pip
try:
    import mysql.connector
except:
    os.system("pip install mysql-connector-python")
    import mysql.connector
#look into subqeuiers
#views
def callD(str):
    return(str)


def serverConnect(host_name, user_name, user_password, program_data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=program_data
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
def printhello():
    x = "functioncalltest"
    print("finmction workds")
    print(callD(x))
    
def onStart(connection):
    mycursor = connection.cursor()

    sql = "DELETE FROM client_room;"
    mycursor.execute(sql)
    connection.commit()

def setRoom(connection, clientid):
    mycursor = connection.cursor()
    sql = "INSERT INTO chatroom.client_room (room_id, client_id) VALUES (%s, %s)"
    val = (1, clientid)
    mycursor.execute(sql, val)
    connection.commit()


def roomChange(connection, client, nRoom):
    mycursor = connection.cursor()
    #print(connection)
    #print(client)
    #print(nRoom)
    sql = "SELECT * FROM chatroom.client_room WHERE client_id = %s;"
    li = (client,)
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    roomid = myresult[1]
    print("CHANGEROOM CURRENT ROOM:", roomid)
    sql = "UPDATE chatroom.client_room SET room_id = %s WHERE client_id = %s"
    roomva = (nRoom, client)
    mycursor.execute(sql, roomva)
    connection.commit()
    sql = "SELECT * FROM chatroom.client_room WHERE room_id = %s;"
    li = (roomid,)
    mycursor.execute(sql, li)
    myresult = mycursor.fetchall()
    return myresult

def historyAdd(connection, client_id, message):
    dt = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    mycursor = connection.cursor()
    li = (client_id,)
    sql = "SELECT * FROM chatroom.client_room WHERE client_id = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    #TODO remove this statement when fixed
    sql = "INSERT INTO chatroom.history (room_id, client_id, message1, time_date) VALUES (%s, %s, %s, %s)"
    val = (myresult[1], myresult[0],message, dt)
    mycursor.execute(sql, val)
    connection.commit()
    return (mycursor.rowcount, "History added.")
    #get room number and time before adding to historyAdd


def clientRoomRemove(connection, clientid):
    mycursor = connection.cursor()
    sql = "DELETE FROM chatroom.client_room WHERE client_id = %s"
    clientidd = (clientid, )
    mycursor.execute(sql, clientidd)
    connection.commit()




def clientRoomSearch(connection ,clientid):
    #return a list of client ids in a room based on a client/client id (returned list should be full)
    mycursor = connection.cursor()
    sql = "SELECT * FROM chatroom.client_room WHERE client_id = %s;"
    li = (clientid,)
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    roomid = myresult[1]
    sql = "SELECT * FROM chatroom.client_room WHERE room_id = %s;"
    li = (roomid,)
    mycursor.execute(sql, li)
    myresult = mycursor.fetchall()
    return myresult





def onOffUser(connection, client, active):
    #set a clients status as active or inactive
    pass
    
def createAccount(connection, email, username, password, ip):
    #print("account creation start")
    mycursor = connection.cursor()
    username = username.replace(" ", "")
    email = email.replace(" ", "")
    li = (username,)
    sql = "SELECT count(1) FROM chatroom.clients WHERE nickname = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    #print(myresult)
    if ipValidate(connection, ip) == "INVALIDIP":
        #print("create account ip invalid")
        return "INVALIDIP"
    if myresult[0] == 1:
        #print("exit stage 1")
        exit()
        return "nonvalid username"
    else:
        mycursor = connection.cursor()
        li = (email,)
        sql = "SELECT count(1) FROM chatroom.login_data WHERE email = %s;"
        mycursor.execute(sql, li)
        myresult = mycursor.fetchone()

        if myresult[0] == 1:
            #print("exit stage 2")
            exit()
            return "nonvalid email"

        else:
            sql = "INSERT INTO chatroom.clients (nickname, active) VALUES (%s, %s)"
            val = (username, 0)
            mycursor.execute(sql, val)
            connection.commit()
            li = (username,)
            sql = "SELECT * FROM chatroom.clients WHERE nickname = %s;"
            mycursor.execute(sql, li)
            myresult = mycursor.fetchone()
            #print(myresult)
            userId = myresult[0]
            sql = "INSERT INTO chatroom.login_data (client_id, email, password) VALUES (%s, %s, %s)"
            val = (userId, email, password)
            mycursor.execute(sql, val)
            connection.commit()

    #print("current end of chatroom account creatiun")
    #exit()
    return "VALID" #+ str(myresult)
    
def accountCheck(connection, email): # returns 0/1 if email doesnt/does exit in db
    mycursor = connection.cursor()
    li = (email,)
    sql = "SELECT count(1) FROM chatroom.login_data WHERE email = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    return myresult[0]
    
def loginSystem(connection, email, passHash, ip):
    mycursor = connection.cursor()
    li = (email,)
    sql = "SELECT * FROM chatroom.login_data WHERE email = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    if ipValidate(connection,ip) == "VALID":
        if myresult != None:
            if passHash == myresult[3]:
                li = (myresult[1],)
                sql = "SELECT * FROM chatroom.clients WHERE client_id = %s;"
                mycursor.execute(sql, li)
                username = mycursor.fetchone()
                new = []
                for i in myresult:
                    new.append(str(i))
                new.append(username[1])
                strr = " ".join(new)
                return "VALID"+"||" + strr
            else:
                return "PASSWRONG"
        else:
            return "NOUSER"
    else:
        return "INVALIDIP"

def ipValidate(connection,ipAdd):
    cursor = connection.cursor()
    li = (ipAdd,)
    sql = "SELECT COUNT(1) FROM chatroom.banned_ips WHERE ipaddress = %s;"
    cursor.execute(sql, li)
    result = cursor.fetchone()
    if result[0] == 1:
        return "INVALIDIP"
    elif result[0] == 0:
        return "VALID"




def ipLogger(connection, userid, ip):
    print(ip)
    cursor = connection.cursor()
    dt = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    sql = "INSERT into chatroom.ip_logs (client_id, ip_add, time_date) VALUES (%s, %s, %s)"
    val = (userid, ip, dt)
    cursor.execute(sql, val)
    connection.commit()