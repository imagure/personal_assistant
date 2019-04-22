"""
@author: ricardo imagure
"""
import spacy
import json
from . import Agglutinator
from semanticizer import entity_class as ec

with open("configs/semanticizer_literals.json") as f:
    data = json.load(f)

n_tags = data["noun_tags"]+data["prop_tags"]+data["adj_tags"]+data["num_tags"]
v_tags = data["verb_tags"]
prop_tags = data["prop_tags"]


class SpacySemanticizer:

    def __init__(self, text, model):
        self.input_text = text
        self.text = model(text)
        self.entities_list = []

    def get_entities(self):

        self.search_chunks()
        agglutinator = Agglutinator.Agglutinator(self.input_text, self.entities_list)
        self.entities_list = agglutinator.agglutinate()

        print("\n", "-" * 20, "> SpacySemanticizer")
        for entity in self.entities_list:
            print(entity)

        return self.entities_list

    def search_chunks(self):
        for token in self.text:
            if token.pos_ in n_tags or token.pos_ in v_tags:
                self.filter_chunk(token)

    def filter_chunk(self, token):
        if token.pos_ in n_tags:
            entity = ec.Entity(text=token.text, start=token.idx, end=(token.idx+len(token.text)), tag='NP', pos=token.pos_)
            self.entities_list.append(entity)

        #if token.pos_ == "VERB" and token.text == 'vem':
        #    entity = ec.Entity(text=token.text, start=token.idx, end=(token.idx+len(token.text)), tag='VP', pos=token.pos_)
        #    self.entities_list.append(entity)
