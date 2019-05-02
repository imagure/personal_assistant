import json
import time

import rdflib
import spacy
from nltk.corpus import wordnet

with open("configs/wordnet.json") as f:
    data = json.load(f)


class Initializer(object):
    sm_ontology = "db/Ontology/assistant2.owl"

    place_synsets_list = []
    commitment_synsets_list = []
    people_synsets_list = []
    graph = rdflib.Graph()
    # spacy_pt = None
    spacy_en = None

    def __init__(self):
        pass

    def set_spacy_models(self):
        start = time.time()
        self.spacy_en = spacy.load('en_core_web_sm')
        # self.spacy_pt = spacy.load('pt_core_news_sm')
        end = time.time()
        print("--> Tempo para set_spacy_models: ", end-start, " s")

    def set_ontology(self, ontology):
        start = time.time()
        self.graph.parse(ontology, format='ttl')
        end = time.time()
        print("--> Tempo para graph parsing: ", end-start, " s")

    def set_synsets(self):
        start = time.time()
        for i in range(len(data["WordNet"]["commitment_synsets"])):
            self.commitment_synsets_list.append(wordnet.synset(data["WordNet"]["commitment_synsets"][i]))
        for i in range(len(data["WordNet"]["place_synsets"])):
            self.place_synsets_list.append(wordnet.synset(data["WordNet"]["place_synsets"][i]))
        for i in range(len(data["WordNet"]["people_synsets"])):
            self.people_synsets_list.append(wordnet.synset(data["WordNet"]["people_synsets"][i]))
        end = time.time()
        print("--> Tempo para set_synsets: ", end - start, " s")
