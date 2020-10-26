import mysql.connector
from mysql.connector import Error

def connectToHost(hostsql, usersql, passwordsql,): # Connects to host
    try:
        connection = mysql.connector.connect(host= hostsql,
                                            user= usersql,
                                            password= passwordsql)

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print('Connected to MySQL Server version ', db_Info)
            cursor = connection.cursor()

    except mysql.connector.Error as e:
        print('Error while connecting to MySQL', e)
        cursor = None
        connection = None

    return connection, cursor

def closeConectionToHost(connection, cursor): # Closes connection to host
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print('MySQL connection is closed')

def executeQuery(connection, cursor, dataBaseName, query): # Runs Query in dataBase

    try:
        if connection.is_connected():
            if query[1] == None:
                cursor.execute(query[0])
            else:
                cursor.execute(query[0], query[1])
                connection.commit() # Important so the query is executed

            print(query[2])

    except mysql.connector.Error as e:
        print(f'Error running Query in {dataBaseName} Data Base in MySQL', e)