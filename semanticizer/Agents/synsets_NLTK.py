from nltk.corpus import wordnet
import json
import time

with open("configs/wordnet.json") as f:
    data = json.load(f)


class NLTKSynsets(object):
    def __init__(self):
        self.place_synsets_list = []
        self.commitment_synsets_list = []
        self.people_synsets_list = []
        start = time.time()
        self.set_synsets()
        end = time.time()
        print("--> Tempo para setar synsets: ", end-start, " s")

    def set_synsets(self):
        for i in range(len(data["WordNet"]["synsets_list"])):
            self.commitment_synsets_list.append(wordnet.synset(data["WordNet"]["commitment_synsets"][i]))
            self.place_synsets_list.append(wordnet.synset(data["WordNet"]["place_synsets"][i]))
            self.people_synsets_list.append(wordnet.synset(data["WordNet"]["people_synsets"][i]))
