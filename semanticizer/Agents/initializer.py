from nltk.corpus import wordnet
import json
import time
import rdflib

with open("configs/wordnet.json") as f:
    data = json.load(f)


class Initializer(object):
    sm_ontology = "db/Ontology/assistant.owl"

    def __init__(self):
        self.place_synsets_list = []
        self.commitment_synsets_list = []
        self.people_synsets_list = []
        self.graph = rdflib.Graph()
        start = time.time()
        self.set_synsets()
        end = time.time()
        print("--> Tempo para setar synsets: ", end-start, " s")

    def set_ontology(self, sm_ontology):
        start = time.time()
        self.graph.parse(sm_ontology, format='ttl')
        end = time.time()
        print("--> Tempo para graph parsing: ", end-start, " s")

    def set_synsets(self):
        for i in range(len(data["WordNet"]["commitment_synsets"])):
            self.commitment_synsets_list.append(wordnet.synset(data["WordNet"]["commitment_synsets"][i]))
        for i in range(len(data["WordNet"]["place_synsets"])):
            self.place_synsets_list.append(wordnet.synset(data["WordNet"]["place_synsets"][i]))
        for i in range(len(data["WordNet"]["people_synsets"])):
            self.people_synsets_list.append(wordnet.synset(data["WordNet"]["people_synsets"][i]))
