import mysql.connector
import time
import datetime
#look into subqeuiers
#views

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
    print("finmction workds")
    
    
def roomChange(client, cRoom, nRoom):
    #change clients room id
    pass


def historyAdd(connection, client_id, message):
    dt = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    mycursor = connection.cursor()
    li = (client_id,)
    sql = "SELECT * FROM chatroom.client_room WHERE client_id = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    sql = "INSERT INTO chatroom.history (room_id, client_id, message1, time_date) VALUES (%s, %s, %s, %s)"
    val = (myresult[1], myresult[0],message, dt)
    mycursor.execute(sql, val)
    connection.commit()
    return (mycursor.rowcount, "History added.")
    #get room number and time before adding to historyAdd
def clientRoomSearch(connection ,client):
    #return a list of client ids in a room based on a client/client id (returned list should be full)
    pass
def onOffUser(connection, client, active):
    #set a clients status as active or inactive
    pass
    
def createAccount():
    pass
    
def accountCheck(connection, email): # returns 0/1 if email doesnt/does exit in db
    mycursor = connection.cursor()
    li = (email,)
    sql = "SELECT count(1) FROM chatroom.login_data WHERE email = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    return myresult[0]
    
def loginSystem(connection, email, passHash):
    print(connection,email,passHash)
    mycursor = connection.cursor()
    li = (email,)
    sql = "SELECT * FROM chatroom.login_data WHERE email = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    if myresult != None:
        if passHash == myresult[3]:
            return "VALID"+ str(myresult)
        else:
            return "PASSWRONG"
    else:
        return "NOUSER"
        
        
 