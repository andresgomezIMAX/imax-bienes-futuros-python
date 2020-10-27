import pandas as pd

projects = pd.read_json('dataProjects.json')
projects = projects[:]['DataProjects']
projects = pd.DataFrame(projects.values.tolist())
print(projects)

tasacion = pd.read_json('dataTasaciones.json')
tasacion = tasacion[:]['DataTasaciones']
tasacion = pd.DataFrame(tasacion.values.tolist())
print(tasacion)