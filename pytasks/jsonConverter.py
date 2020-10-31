import pandas as pd

def recibeJson(filePath):
    dfFile = pd.read_json(filePath)
    dfFile = dfFile[:]['DataProjects']
    dfFile = pd.DataFrame(dfFile.values.tolist())
    
    return dfFile

def sentJson(dfFile, name):

    columnas = ['DataProjects', 'Message', 'StatusCode']

    newFile = pd.DataFrame(columns= columnas)

    for x in dfFile.index:
            
        data = {
                'DataProjects': dfFile.loc[x], 'Message': '', 'StatusCode': 200
                }

        newFile = newFile.append(data, ignore_index=True)

    newFile.to_json(f'{name}.json')

if __name__ == '__main__':
    df = recibeJson('dataGeneral.json')
    # df = pd.read_json('dataGeneral.json')
    sentJson(df, 'dataGeneral')
    df = recibeJson('dataUITasa.json')
    # df = pd.read_json('dataUITasa.json')
    sentJson(df, 'dataUITasa')
