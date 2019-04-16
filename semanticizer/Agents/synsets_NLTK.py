from nltk.corpus import wordnet
import json
import time

with open("configs/wordnet.json") as f:
    data = json.load(f)


class NLTKSynsets(object):
    def __init__(self):
        self.synsets_list = []
        start = time.time()
        self.set_synsets()
        end = time.time()
        print("--> Tempo para setar synsets: ", end-start, " s")

    def set_synsets(self):
        for i in range(len(data["WordNet"]["synsets_list"])):
            self.synsets_list.append(wordnet.synset(data["WordNet"]["synsets_list"][i]))
