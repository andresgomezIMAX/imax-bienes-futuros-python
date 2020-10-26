from MySqlConector import connectToHost, closeConectionToHost, executeQuery

def createDataBase(hostsql, usersql, passwordsql, dataBaseName, tableName):

    connection, cursor = connectToHost(hostsql, usersql, passwordsql) # Init connection

    # Create DataBase
    data = None
    menssage = f'Data Base {dataBaseName} created!'
    command = f'CREATE DATABASE {dataBaseName};'
    query = (command, data, menssage)
    executeQuery(connection, cursor, dataBaseName, query)

    # Use dataBase
    data = None
    menssage = f"You're connected to database: {dataBaseName}!"
    command = f'USE {dataBaseName};'
    query = (command, data, menssage)
    executeQuery(connection, cursor, dataBaseName, query)

    #Create Table
    data = None
    columnsNames = """unidad VARCHAR(255), num VARCHAR(255), nivel VARCHAR(255), 
                    dni VARCHAR(255), nombre VARCHAR(255), terreno FLOAT, ocupada FLOAT, 
                    techada FLOAT, comunes FLOAT, moneda VARCHAR(255), valor FLOAT, terrenousd FLOAT, 
                    edifusd FLOAT, comercialusd FLOAT, realizausd FLOAT, asegurausd FLOAT, tipocambio FLOAT, fecha DATE,
                    clase VARCHAR(255), vueusd FLOAT, tipo VARCHAR(255), descripción VARCHAR(255)"""
    menssage = f'Table {tableName} created!'
    command = f"""CREATE TABLE {tableName} ({columnsNames});"""
    query = (command, data, menssage)
    executeQuery(connection, cursor, dataBaseName, query)

    tableName = 'tasaciones'
    command = f"""CREATE TABLE {tableName} ({columnsNames});"""
    query = (command, data, menssage)
    executeQuery(connection, cursor, dataBaseName, query)

    closeConectionToHost(connection, cursor) # Close connection


if __name__ == '__main__':
    
    # Server connection informartion:
    hostsql = 'localhost'
    usersql = 'root'
    passwordsql = 'acidbass'

    # DataBase main info:
    dataBaseName = 'proyecto1'#input('Nombre de base de datos: ')
    tableName = 'matriz'

    createDataBase(hostsql, usersql, passwordsql, dataBaseName, tableName)