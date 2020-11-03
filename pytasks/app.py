from flask import Flask, jsonify, request
import pandas as pd
from createMatrixJson import createMatrix
from jsonConverter import sentJson, recibeJson
from createExcelMatrixJson import createExcelMatrix
from createInformeJson import createExcelInforme

app = Flask(__name__)

 
@app.route ('/')
def index(): 
    return jsonify({"message": "hola"})


@app.route('/newMatrix')    
def newMatrix():
    projects = recibeJson("http://localhost:8000/api/v1/proyectos/list")
    
    projectSelected = 0 # Indice donde se encuentra el proyecto seleccionado

    mainDataFilePath = projects['PathData'][projectSelected] # Excel with matrix data
    formatFile = projects['PathInforme'][projectSelected] # Excel with project data
   
    matrix = createMatrix(mainDataFilePath, formatFile) # Crea Matriz de tasaciones y devuelve json

    name = 'matrixjson.json' # Ubicación donde se guardará el archivo json y nombre del archivo

    sentJson(matrix, name)
    
@app.route('/excelMatrix')    
def excelMatrix():
    projects = recibeJson("http://localhost:8000/api/v1/proyectos/list")
    
    projectSelected = 0 # Indice donde se encuentra el proyecto seleccionado

    mainDataFilePath = projects['PathData'][projectSelected] # Excel with matrix data
    formatFile = projects['PathInforme'][projectSelected] # Excel with project data

    formatMatrixFile = 'Formatos\MATRIZ TASACIONES.xlsx' # Ubicación formato de matriz de tasaciones
    
    pathmatrix = 'matrixjson.json' # Ubicación donde se guardará el archivo json y nombre del archivo

    pathExcel = '' # Ubicación dónde se desea guardar el excel resultante
   
    createExcelMatrix(formatMatrixFile, formatFile, pathmatrix, pathExcel) # Crea Matriz de tasaciones y devuelve json

@app.route('/excelInforme')    
def excelInforme():
    projects = recibeJson("http://localhost:8000/api/v1/proyectos/list")
    
    projectSelected = 0

    mainDataFilePath = projects['PathData'][projectSelected] # Excel with matrix data
    formatFile = projects['PathInforme'][projectSelected] # Excel with project data

    formatReportfile = 'Formatos\Informe.xlsx' #Ubicación de formato para informe

    pathmatrix = 'matrixjson.json'
    pathdatageneral = 'dataGeneral.json'
    pathdatauitasa = 'dataUITasa.json'

    pathExcel = '' # Ubicación dónde se desea guardar el excel resultante

    tasacionSegui, DataOutMatrix = createExcelInforme(pathdatauitasa, formatFile, mainDataFilePath, formatReportfile, pathmatrix, pathdatageneral, pathExcel)

    nameT = 'tasaciones.json'
    nameM = 'matrixUpdatejson.json'

    sentJson(tasacionSegui, nameT)
    sentJson(DataOutMatrix, nameM)

# @app.route('/projects/<string:project_unidad>')
# def getProject(project_unidad):
#     print (project_unidad)
#     return 'received'

# @app.route('/projects/<string:project_direccion>')
# def getProjectid(project_direccion):
#     projectsFound = [project for project in projects if project['direccion'] == project_direccion]
#     return jsonify({"project": projectsFound[0]})


# @app.route('/projects', methods=['POST'])
# def addProjects():
#     new_project = {
#         "idProyecto": request.json['idProyecto'],
#         "nombreProyecto": request.json['nombreProyecto'],
#         "direccion": request.json['direccion'],
#         "promotor": request.json['promotor'],
#         "banco": request.json['banco']
#     }

#     projects.append(new_project)
#     return jsonify({"message": "Proyecto agregado correctamente"})



# @app.route('/projects/<string:project_nombreProyecto>', methods=['PUT'])
# def editProject(project_nombreProyecto):
#     projectFoundID= [project for project in projects if project['nombreProyecto'] == project_nombreProyecto]
#     if(len(projectFoundID) > 0):
#         projectFoundID[0]['nombreProyecto'] = request.json['nombreProyecto']
#         return jsonify ({
#             "message": "Proyecto actualizado",
#             "project": projectFoundID[0]
#         })
#     return jsonify ({"message": "nombreProyecto no encontrado"})    



# @app.route('/projects/<string:project_nombreProyecto>', methods=['DELETE'])
# def deleteProject(project_nombreProyecto):
#     projectFoundID= [project for project in projects if project['nombreProyecto'] == project_nombreProyecto]
#     if(len(projectFoundID) > 0):
#         projects.remove(projectFoundID[0])
#         return jsonify({
#             "message": "proyecto eliminado",
#             "projects": projects
#         })
#     return jsonify ({"message": "nombreProyecto no encontrado"})



if __name__ == '__main__': #si es el archivo principal, ejecutalo
    app.run(debug=True)