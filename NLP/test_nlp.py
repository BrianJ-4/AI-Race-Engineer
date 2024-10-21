import spacy
import sys
from actions import *

def main():
    intentModel = LoadModel("NLP/intent_classification/intent_model")
    nerModel = LoadModel("NLP/ner/ner_model")
    while 0 < 1:
        inputString = input("Enter input: ")
        if inputString == "q" or inputString == "Q":
            break
        intent = PredictIntent(intentModel, nerModel, inputString)
        if intent == "ask_damage" or intent == "ask_temperature":
            data = RecognizeEntities(nerModel, inputString, intent)
        else:
            data = intent
        PerformAction(data)

def PredictIntent(intentModel, nerModel, text):
    doc = intentModel(text)
    maxScore = 0.0
    maxIntent = None
    for intent, score in doc.cats.items():
        if score > maxScore:
            maxIntent = intent
            maxScore = score
    return maxIntent
    

def RecognizeEntities(nlp, text, intent):
    doc = nlp(text)
    data = {
        "INTENT" : intent,
        "DIRECTION" : "",
        "SIDE" : "",
        "PART" : ""
    }
    for ent in doc.ents:
        data[ent.label_] = ent.text
    return data

def LoadModel(dir):
    model = spacy.load(dir)
    return model

main()