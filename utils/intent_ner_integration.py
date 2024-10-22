from utils.load_models import *

# Load models once at the beginning
intent_model = LoadIntentModel()
ner_model = LoadNERModel()

def ProcessInput(input_string):
    # Get intent from intent classifier
    intent = PredictIntent(intent_model, input_string)

    # If intent requires NER, pass input to NER model
    if intent in ["ask_damage", "ask_temperature"]:
        data = RecognizeEntities(ner_model, input_string, intent)
    else:
        data = {"INTENT": intent}
    return data

def PredictIntent(intent_model, text):
    doc = intent_model(text)
    max_score = 0.0
    max_intent = None
    
    # Find intent with highest confidence score
    for intent, score in doc.cats.items():
        if score > max_score:
            max_intent = intent
            max_score = score

    return max_intent

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