from MySqlConector import connectToHost, closeConectionToHost, executeQuery
from createDataBase import createDataBase
import pandas as pd
import openpyxl

def createMatrix(hostsql, usersql, passwordsql, dataBaseName, tableName, mainDataFilePath, formatFile): # Uploads to table Matriz the data form users excels and makes the necesary calculus

    #Gets from main excel and real estate units sheet data
    DataInMatrix = pd.read_excel(mainDataFilePath, sheet_name='MATRIZ')
    DataInMatrix.fillna(value = 0, inplace = True)

    unidad = DataInMatrix.iloc[:]['Unidad Inmobiliaria'] #Type of real estate unit
    num = DataInMatrix.iloc[:]['No'] #Number of real estate unit in the project
    nivel = DataInMatrix.iloc[:]['Nivel ']
    aOcupada = DataInMatrix.iloc[:]['Área ocupada (m²)']
    aTechada = DataInMatrix.iloc[:]['Área techada (m²)']
    moneda = DataInMatrix.iloc[:]['Moneda']
    vVenta = DataInMatrix.iloc[:]['Valor de Venta']
    vista = DataInMatrix.iloc[:]['VISTA']

    #Gets from main excel and project sheet data
    DataInGeneral = pd.read_excel(mainDataFilePath, sheet_name='DATA')

    vut = float(DataInGeneral.iloc[:1]['VUT (USD)']) #Unit terrain value
    vrc = float(DataInGeneral.iloc[:1]['VRC (USD)']) #Unit reconstruction value
    tc = float(DataInGeneral.iloc[:1]['TC']) #Exchange rate

    #Gets from report format file the name of the financial compañy / main client
    wbProyecto = openpyxl.load_workbook(formatFile, read_only=True)
    sheetProyecto = wbProyecto['Memoria']
    eFinan = sheetProyecto['D7'].value
    wbProyecto.close

    vue2 = DataInGeneral[['VUE (USD)', 'Tipo', 'Descripción']]
    vue = vue2.rename(index = DataInGeneral.iloc[:]['Clase']) #Gets type of real estate unit data

    connection, cursor = connectToHost(hostsql, usersql, passwordsql) # Init connection

    # Use dataBase
    data = None
    menssage = f"You're connected to database: {dataBaseName}!"
    command = f'USE {dataBaseName};'
    query = (command, data, menssage)
    executeQuery(connection, cursor, dataBaseName, query)

    command = (
                f"""INSERT INTO {tableName} (unidad, num, nivel, dni, nombre,
                terreno, ocupada, techada, comunes, moneda, valor, 
                terrenousd, edifusd, comercialusd, realizausd,
                asegurausd, tipocambio, fecha, clase, vueusd, tipo, descripción)"""
                """VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                )

    #Runs true al the data and uploads it to the database MySql
    for x in range(0, len(DataInMatrix), 1):

        #Init internal calculus:
        aTerreno = round(float(aOcupada[x]) / 20 * 1.4, 2) #Implementar ingreso de factores 20 y 1.4
        aComunes = round(float(aTechada[x]) * 0.15, 2) #Implementar ingreso de factores 0.15
        vTerrenoUsd = round(aTerreno * vut / 100, 0) * 100
        if unidad[x] == 'Departamento':
            vComercialUsd = round( 
                                    float(vue.loc[vista[x]]['VUE (USD)']) * (float(aTechada[x]) +
                                    ((float(aOcupada[x]) - float(aTechada[x])) * 0.3)) / 100, 0
                                ) * 100
        else:
            vComercialUsd = vue.loc[vista[x]]['VUE (USD)']

        vEdificaUsd = vComercialUsd - vTerrenoUsd
        vRealizaUsd = round(vComercialUsd * 0.8 / 100, 0) *100

        if eFinan == 'BANCO INTERNACIONAL DEL PERÚ S.A.A. - INTERBANK':
            iAseguraUsd = vComercialUsd
        else:
            iAseguraUsd = round(
                                float(aTechada[x]) * vrc * 1.15 / 100,
                                0
                            ) * 100
        #Finish internal calculus

        #Init Check calculus:
        # if moneda[x] == 'Soles':
        #     vVentaUSD = float(vVenta[x]) / tc
        # else:
        #     vVentaUSD = float(vVenta[x])
        
        # errorCheck = False

        # if vComercialUsd < vVentaUSD:
        #     print(f"""Para el {unidad[x]} {num[x]} el valor comercial (USD {vComercialUsd} - ratio usado {vue.loc[vista[x]]['VUE (USD)']}) 
        #             es menor que el valor de venta (USD {round(vVentaUSD, 2)} - ratio precio USD {round(vVentaUSD/float(aTechada[x]),2)}). 
        #             Revisar datos de excel inicial y volver a subir""")
        #     errorCheck = True

        # revisionPorcentual = round(vComercialUsd / vVentaUSD - 1,2)

        # if revisionPorcentual > 0.10:
        #     print(f"""Para el {unidad[x]} {num[x]} el valor comercial (USD {vComercialUsd} - ratio usado {vue.loc[vista[x]]['VUE (USD)']}) 
        #             es mayor que el valor de venta (USD {round(vVentaUSD, 2)} - ratio precio USD {round(vVentaUSD/float(aTechada[x]),2)}) en un {revisionPorcentual*100}%, 
        #             siendo que máximo deberia ser un 5%. 
        #             Revisar datos de excel inicial y volver a subir""")
        #     errorCheck = True

        # if errorCheck == True:
        #     menssage = f'\nSe reinicia base de datos...'
        #     command = f'DROP DATABASE {dataBaseName}'
        #     query = (command, data, menssage)
        #     executeQuery(connection, cursor, dataBaseName, query) #Runs Query
        #     closeConectionToHost(connection, cursor) # Close connection

        #     createDataBase(hostsql, usersql, passwordsql, dataBaseName, tableName)
            
        #     break
        #     exit()
        #Finish Check calculus
        
        data = (
                unidad[x], str(num[x]), str(nivel[x]), None, None, float(aTerreno),
                float(aOcupada[x]), float(aTechada[x]), float(aComunes), moneda[x], 
                float(vVenta[x]), float(vTerrenoUsd), float(vEdificaUsd), float(vComercialUsd),
                float(vRealizaUsd), float(iAseguraUsd), float(tc), None, 
                vista[x], float(vue.loc[vista[x]]['VUE (USD)']), vue.loc[vista[x]]['Tipo'], vue.loc[vista[x]]['Descripción']
                )

        menssage = f'Tabla de matriz actualizada con {unidad[x]} {num[x]},  satisfactoriamente!'

        query = (command, data, menssage)
        executeQuery(connection, cursor, dataBaseName, query) #Runs Query

    closeConectionToHost(connection, cursor) # Close connection

if __name__ == '__main__':

    # Server connection informartion:
    hostsql = 'localhost'
    usersql = 'root'
    passwordsql = 'acidbass'

    mainDataFilePath = 'pytasks\Formatos\DATA.xlsx' # Excel with matrix data
    formatFile = 'pytasks\Formatos\PMF-Tasación.xlsx' # Excel with project data

    dataBaseName = 'proyecto1'#input('Nombre de base de datos: ')
    tableName = 'matriz' #table with project matrix data

    createMatrix(hostsql, usersql, passwordsql, dataBaseName, tableName, mainDataFilePath, formatFile)