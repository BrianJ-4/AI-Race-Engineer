import spacy
from spacy.training import Example
from spacy.util import minibatch
import json

nlp = spacy.blank("en")

if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")

labels = ["DIRECTION", "SIDE", "PART"]
for label in labels:
    ner.add_label(label)

# Train model method
def TrainNERModel(nlp, data, n_iter=20):
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        # Use minibatching to update the model in small batches
        batches = minibatch(data, size=2)
        for batch in batches:
            texts, annotations = zip(*[(entry["text"], entry["entities"]) for entry in batch])
            examples = [Example.from_dict(nlp.make_doc(text), {"entities": entities}) for text, entities in zip(texts, annotations)]
            nlp.update(examples, sgd=optimizer, losses=losses)
        print(f"Losses at iteration {i}: {losses}")

def LoadNERData():
    with open("NLP/ner/training_data/data.json", "r") as file:
        data = json.load(file)
    return data

# Get training data
data = LoadNERData()

# Train and save model
TrainNERModel(nlp, data)
nlp.to_disk("NLP/ner/ner_model")