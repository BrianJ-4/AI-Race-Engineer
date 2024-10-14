import spacy

def main():
    nlp = LoadModel("NLP/intent_classification/model")
    while 0 < 1:
        testString = input("Enter prompt: ")
        if testString == "q" or testString == "Q":
            break
        PredictIntent(nlp, testString)
        print()

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