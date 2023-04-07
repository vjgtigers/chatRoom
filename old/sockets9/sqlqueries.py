import mysql.connector
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
def loginSystem():
    #for if password based accounts ever get implemented
    pass


def historyAdd(client, message):
    #get room number and time before adding to historyAdd
    pass
def clientRoomSearch(client):
    #return a list of clients in a room based on a client/client id (returned list should be full)
    pass
def onOffUser(client, active):
    #set a clients status as active or inactive
    pass
    
def createAccount():
    pass
    
def accountCheck(email, connection): # returns 0/1 if email doesnt/does exit in db
    mycursor = connection.cursor()
    li = (email,)
    sql = "SELECT count(1) FROM chatroom.login_data WHERE email = %s;"
    mycursor.execute(sql, li)
    myresult = mycursor.fetchone()
    return myresult[0]