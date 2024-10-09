import spacy

def main():
    nlp = LoadModel("NLP/models")
    testString = "Who is in front?"
    PredictIntent(nlp, testString)

def LoadModel(dir):
    nlp = spacy.load(dir)
    return nlp

def PredictIntent(nlp, text):
    doc = nlp(text)
    maxScore = 0.0
    maxIntent = None
    for intent, score in doc.cats.items():
        print(f"Intent: {intent}, Confidence: {score}")
        if score > maxScore:
            maxIntent = intent
            maxScore = score
    print()
    print(f"Highest confidence intent: {maxIntent}")

main()