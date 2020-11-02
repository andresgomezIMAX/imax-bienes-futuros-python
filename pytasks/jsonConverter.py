import pandas as pd

def recibeJson(filePath): #Recives json and converts for dataFrame use
    dfFile = pd.read_json(filePath)
    dfFile = dfFile[:]['DataProjects']
    dfFile = pd.DataFrame(dfFile.values.tolist())
    
    return dfFile

def sentJson(dfFile, name): #Recives dataFrame and converts for json read

    json = pd.read_json('Formatos\Template.json')

    data = pd.DataFrame(columns= dfFile.columns)
    for x in dfFile.index:
            data.loc[x] = dfFile.loc[x]

    json = json.drop(index=[1,2,3,4,5,6,7,8,9])
    json['DataProjects'][0] = data

    json.to_json(f'{name}.json', orient='records')
    json = open(f'{name}.json', 'r')
    json.close
    jsontxt = json.read()
    jsontxt = jsontxt[1:len(jsontxt)-1]

    json2 = open(f'{name}.json', 'w')
    json2.write(jsontxt)
    json2.close

if __name__ == '__main__':
    # df = recibeJson('dataGeneral.json')
    # df2 = recibeJson('dataUITasa.json')
    # df = pd.read_json('dataGeneral.json')
    # df2 = pd.read_json('dataUITasa.json')
    # sentJson(df, 'dataGeneral')
    # sentJson(df2, 'dataUITasa')
    pass
