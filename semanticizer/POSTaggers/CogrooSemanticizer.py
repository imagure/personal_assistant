"""
@author: ricardo imagure
"""

from cogroo_interface import Cogroo
from . import Agglutinator
import json
from semanticizer import entity_class as ec

with open("configs/semanticizer_literals.json") as f:
    data = json.load(f)

n_tags = data["noun_tags"]+data["prop_tags"]+data["adj_tags"]+data["num_tags"]
v_tags = data["verb_tags"]
prop_tags = data["prop_tags"]


class CogrooSemanticizer:
    cogroo = Cogroo.Instance()
    entities_list = []

    def __init__(self, text):
        self.input_text = text
        self.pos_tagged_text = self.cogroo.analyze(text).sentences[0]

    def get_entities(self):
        print(self.pos_tagged_text.chunks)
        self.entities_list = self.search_chunks()
        agglutinator = Agglutinator.Agglutinator(self.input_text, self.entities_list)
        self.entities_list = agglutinator.agglutinate()
        self.clean_entities()
        return self.entities_list

    def search_chunks(self):
        for chunk in self.pos_tagged_text.chunks:
            if chunk.tag in n_tags or chunk.tag in v_tags:
                self.entities_list = self.filter_chunk(chunk)
        return self.entities_list

    def filter_chunk(self, chunk):
        '''
        Retira expressões das frases
        :param chunk:
        :param self.entities_list:
        :return: entities_list:
        '''
        for token in chunk.tokens:

            if token.pos in n_tags:
                entity = ec.Entity(text=token.lexeme, start=token.start, end=token.end, tag='NP', pos=token.pos)
                self.entities_list.append(entity)

            if token.pos in v_tags and token.lexeme == 'vem':
                entity = ec.Entity(text=token.lexeme, start=token.start, end=token.end, tag='VP', pos=token.pos)
                self.entities_list.append(entity)

        return self.entities_list

    def clean_entities(self):
        for entity in self.entities_list:
            if entity.pos in prop_tags:
                text = entity.text.replace('_', ' ')
                entity.text = text
