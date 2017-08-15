import json

def loadJson(pathToFile):
    with open(pathToFile, encoding = 'utf-8') as jsonFile:
        data = json.load(jsonFile)
    return data
