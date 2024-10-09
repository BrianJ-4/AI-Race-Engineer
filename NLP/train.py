import json
import spacy
from spacy.training import Example
from spacy.util import minibatch

nlp = spacy.blank('en')

textcat = nlp.add_pipe('textcat')

categories = ["ask_position_ahead", "ask_tire_status", "ask_weather", "ask_last_lap_time"]
for category in categories:
    textcat.add_label(category)

def LoadAndCombineData():
    combinedData = []
    for category in categories:
        filename = category + ".json"
        with open("NLP/training_data/" + filename, 'r') as file:
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

data = LoadAndCombineData()
with open('NLP/training_data/full_training_data.json', 'w') as outfile:
    json.dump(data, outfile, indent = 4)

# Train model method
def TrainModel(nlp, data, n_iter = 10):
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        # Use minibatching to update the model in small batches
        batches = minibatch(data, size = 2)
        for batch in batches:
            texts, annotations = zip(*[(entry["text"], entry["cats"]) for entry in batch])
            examples = [Example.from_dict(nlp.make_doc(text), {"cats": cats}) for text, cats in zip(texts, annotations)]
            nlp.update(examples, sgd = optimizer, losses = losses)
        print(f"Losses at iteration {i}: {losses}")

# Train model
TrainModel(nlp, data)

# Test
doc = nlp("Who is in the position ahead of me?")

# Print all predicted intents and corresponding confidence scores
print()
for intent, score in doc.cats.items():
    print(f"Intent: {intent}, Confidence: {score}")
