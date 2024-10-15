import spacy

def main():
    nlp = LoadModel("NLP/ner/ner_model")
    while 0 < 1:
        testString = input("Enter prompt: ")
        if testString == "q" or testString == "Q":
            break
        RecognizeEntities(nlp, testString)
        print()

def LoadModel(dir):
    nlp = spacy.load(dir)
    return nlp

def RecognizeEntities(nlp, text):
    doc = nlp(text)
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")

main()