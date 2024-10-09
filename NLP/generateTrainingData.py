import json
import os

def GetCategories():
    path = "NLP/training_data/intents"
    categoryFiles = os.listdir(path)
    categories = []
    for category in categoryFiles:
        category = category.replace(".json", "")
        categories.append(category)
    return categories

def LoadAndCombineData():
    categories = GetCategories()
    combinedData = []
    for category in categories:
        filename = category + ".json"
        with open("NLP/training_data/intents/" + filename, 'r') as file:
            data = json.load(file)
            intentData = AddAllCategories(data, categories)
            combinedData.extend(intentData)
    return combinedData

def AddAllCategories(intentData, categories):
    for entry in intentData:
        cats = entry["cats"]
         # Add missing categories and set their value to 0
        for category in categories:
            if category not in cats:
                cats[category] = 0
    return intentData

def GenerateData():
    data = LoadAndCombineData()
    with open('NLP/training_data/full_training_data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def LoadData():
    with open('NLP/training_data/full_training_data.json', 'r') as file:
        data = json.load(file)
    return data

GenerateData()