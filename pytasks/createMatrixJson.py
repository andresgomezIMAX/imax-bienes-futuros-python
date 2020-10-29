import pandas as pd
import openpyxl

def createMatrix(mainDataFilePath, formatFile): # Cretaes JSSON table Matriz data form users excels and makes the necesary calculus

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
    tipo = DataInMatrix.iloc[:]['TIPO']
    totalesData = DataInMatrix.sum(axis=0, skipna=True) #Sum all data in columns
    aOcupadaSum = totalesData['Área ocupada (m²)']

    #Gets from main excel and project sheet data
    DataInGeneral = pd.read_excel(mainDataFilePath, sheet_name='DATA')

    vut = float(DataInGeneral.iloc[:1]['VUT (USD)']) #Unit terrain value
    vrc = float(DataInGeneral.iloc[:1]['VRC (USD)']) #Unit reconstruction value
    tc = float(DataInGeneral.iloc[:1]['TC']) #Exchange rate
    factorRealiza = float(DataInGeneral.iloc[:1]['F.Realiza (%)']) #Realization value factor for calculus
    factorAsegura = float(DataInGeneral.iloc[:1]['F.Asegura (%)']) #Insurable value factor for calculus
    aComunTotal = float(DataInGeneral.iloc[:1]['A. Común (m²)']) #Projects Total Comun area
    factorTasacion = DataInGeneral.iloc[:3][['Tipo Unidad', '% Tasación']]
    
    aOcupadaTotal = aOcupadaSum + aComunTotal #Total area including comun area

    #Gets from report format file the name of the financial compañy / main client and land area
    wbProyecto = openpyxl.load_workbook(formatFile, read_only=True)
    sheetProyecto = wbProyecto['Memoria']
    eFinan = sheetProyecto['D7'].value
    aTerrenoPredio = float(sheetProyecto['P94'].value)
    wbProyecto.close

    claseUI = DataInGeneral[['Tipo', 'Descripción']]
    claseUI = claseUI.rename(index = DataInGeneral.iloc[:]['Clase']) #Gets type of real estate unit data

    #Cretaes Matrix
    columnas = [
                'unidad', 'num', 'nivel', 'dni', 'nombre',
                'terreno', 'ocupada', 'techada', 'comunes', 'moneda', 'valor', 
                'terrenousd', 'edifusd', 'comercialusd', 'realizausd',
                'asegurausd', 'tipocambio', 'fecha', 'clase', 'vueusd', 'tipo', 'descripción'
                ]

    matrix = pd.DataFrame(columns= columnas)

    #Runs truew all the data and uploads it to the main DataFrame:
    for x in range(0, len(DataInMatrix), 1):

        #Real estate land area calculus:
        incidenciaComun = aComunTotal / aOcupadaTotal
        aTerrenoComun = incidenciaComun * aTerrenoPredio
        incidencia1 = aOcupada[x] / aOcupadaTotal
        aTerreno1 = incidencia1 * aTerrenoPredio
        incidencia2 = aOcupada[x] / aOcupadaSum
        aTerreno2 = incidencia2 * aTerrenoComun
        aTerreno = round(aTerreno1 + aTerreno2, 2)

        #Real estate Comun area calculus:
        incidencia3 = aTerreno / aTerrenoPredio
        aComunes = round(incidencia3 * aComunTotal, 2)
        
        #Land value for each real estate unit:
        vTerrenoUsd = round(aTerreno * vut / 100, 0) * 100

        #Comercial value for each real estate unit:
        for y in factorTasacion.index:
            if factorTasacion.loc[:y]['Tipo Unidad'][0] == unidad[x]:
                factorT = factorTasacion.loc[:y]['% Tasación'][0]
        
        if moneda[x] == 'Soles':
            vComercialUsd = round((float(vVenta[x]) / tc * (1 + factorT)) / 100, 0) * 100
        else:
            vComercialUsd = round((float(vVenta[x]) * (1 + factorT)) / 100, 0) * 100

        #Unitary comercial value /m2 for each Real Estate Unit:
        vue = vComercialUsd / aTechada[x]

        #Edification value for each real estate unit:
        vEdificaUsd = vComercialUsd - vTerrenoUsd
        
        #Excecution value for each real estate unit:
        vRealizaUsd = round(vComercialUsd * factorRealiza / 100, 0) *100

        #Insurable value for each real estate unit:
        if eFinan == 'BANCO INTERNACIONAL DEL PERÚ S.A.A. - INTERBANK':
            iAseguraUsd = vComercialUsd
        else:
            iAseguraUsd = round(float(aTechada[x]) * vrc * (1 + factorAsegura) / 100, 0) * 100
        
        data = {
                'unidad': unidad[x], 'num': str(num[x]), 'nivel': str(nivel[x]), 'dni': None, 'nombre': None, 'terreno': float(aTerreno),
                'ocupada': float(aOcupada[x]), 'techada': float(aTechada[x]), 'comunes': float(aComunes), 'moneda': moneda[x], 
                'valor': float(vVenta[x]), 'terrenousd': float(vTerrenoUsd), 'edifusd': float(vEdificaUsd), 'comercialusd': float(vComercialUsd),
                'realizausd': float(vRealizaUsd), 'asegurausd': float(iAseguraUsd), 'tipocambio': float(tc), 'fecha': None, 
                'clase': tipo[x], 'vueusd': float(vue), 'tipo': claseUI.loc[tipo[x]]['Tipo'], 'descripción': claseUI.loc[tipo[x]]['Descripción']
                }
        
        matrix = matrix.append(data, ignore_index=True)
        
        print(f'Tabla de matriz actualizada con {unidad[x]} {num[x]},  satisfactoriamente!')

    matrix.to_json('matrixjson.json')

if __name__ == '__main__':

    mainDataFilePath = 'Formatos\DATA.xlsx' # Excel with matrix data
    formatFile = 'Formatos\PMF-Tasacion.xlsx' # Excel with project data

    createMatrix(mainDataFilePath, formatFile)