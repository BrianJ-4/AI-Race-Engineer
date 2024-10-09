from generateTrainingData import *
import spacy
from spacy.training import Example
from spacy.util import minibatch

nlp = spacy.blank('en')

textcat = nlp.add_pipe('textcat')

categories = GetCategories()
for category in categories:
    textcat.add_label(category)

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

# Get training data
data = LoadData()

# Train and save model
TrainModel(nlp, data)
nlp.to_disk("NLP/models")