from nltk.corpus import wordnet
import json

with open("configs/wordnet.json") as f:
    data = json.load(f)


class NLTKSynsets(object):
    def __init__(self):
        self.synsets_list = []
        self.set_synsets()

    def set_synsets(self):
        for i in range(len(data["WordNet"]["synsets_list"])):
            self.synsets_list.append(wordnet.synset(data["WordNet"]["synsets_list"][i]))
