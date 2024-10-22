import spacy

def LoadIntentModel():
    try:
        model = spacy.load("NLP/intent_classification/intent_model")
        print("Intent classification model loaded successfully.")
        return model 
    except Exception as e:
        print(f"Error loading intent classification model: {e}")
        return None

def LoadNERModel():
    try:
        model = spacy.load("NLP/ner/ner_model")
        print("NER model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading NER model: {e}")
        return None