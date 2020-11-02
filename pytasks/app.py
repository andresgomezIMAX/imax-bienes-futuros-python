from flask import Flask, jsonify, request

app = Flask(__name__)

from projects import projects


@app.route ('/')
def index(): 
    return jsonify({"message": "hola bb"})


@app.route('/projects')    
def getProjects():
    return jsonify({"projects": projects})


# @app.route('/projects/<string:project_unidad>')
# def getProject(project_unidad):
#     print (project_unidad)
#     return 'received'

@app.route('/projects/<string:project_direccion>')
def getProjectid(project_direccion):
    projectsFound = [project for project in projects if project['direccion'] == project_direccion]
    return jsonify({"project": projectsFound[0]})


@app.route('/projects', methods=['POST'])
def addProjects():
    new_project = {
        "idProyecto": request.json['idProyecto'],
        "nombreProyecto": request.json['nombreProyecto'],
        "direccion": request.json['direccion'],
        "promotor": request.json['promotor'],
        "banco": request.json['banco']
    }

    projects.append(new_project)
    return jsonify({"message": "Proyecto agregado correctamente"})



@app.route('/projects/<string:project_nombreProyecto>', methods=['PUT'])
def editProject(project_nombreProyecto):
    projectFoundID= [project for project in projects if project['nombreProyecto'] == project_nombreProyecto]
    if(len(projectFoundID) > 0):
        projectFoundID[0]['nombreProyecto'] = request.json['nombreProyecto']
        return jsonify ({
            "message": "Proyecto actualizado",
            "project": projectFoundID[0]
        })
    return jsonify ({"message": "nombreProyecto no encontrado"})    



@app.route('/projects/<string:project_nombreProyecto>', methods=['DELETE'])
def deleteProject(project_nombreProyecto):
    projectFoundID= [project for project in projects if project['nombreProyecto'] == project_nombreProyecto]
    if(len(projectFoundID) > 0):
        projects.remove(projectFoundID[0])
        return jsonify({
            "message": "proyecto eliminado",
            "projects": projects
        })
    return jsonify ({"message": "nombreProyecto no encontrado"})

if __name__ == '__main__': #si es el archivo principal, ejecutalo
    app.run(debug=True)