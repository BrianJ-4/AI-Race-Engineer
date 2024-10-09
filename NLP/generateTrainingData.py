import json

categories = ["ask_position_ahead", "ask_current_position", "ask_weather", "ask_last_lap_time", "ask_track_temperature", "ask_air_temperature"]

def LoadAndCombineData():
    combinedData = []
    for category in categories:
        filename = category + ".json"
        with open("NLP/training_data/intents/" + filename, 'r') as file:
            data = json.load(file)
            intentData = AddAllCategories(data)
            combinedData.extend(intentData)
    return combinedData

def AddAllCategories(intentData):
    for entry in intentData:
        cats = entry["cats"]
         # Add missing categories and set their value to 0
        for category in categories:
            if category not in cats:
                cats[category] = 0
    return intentData

def generateData():
    data = LoadAndCombineData()
    with open('NLP/training_data/full_training_data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def getCategories():
    return categories

def loadData():
    with open('NLP/training_data/full_training_data.json', 'r') as file:
        data = json.load(file)
    return data

generateData()