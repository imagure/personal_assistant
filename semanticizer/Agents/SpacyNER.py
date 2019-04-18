import spacy
from semanticizer import entity_class as ec
import time


class SpacyNER(object):

    def __init__(self, text, model):
        self.input_text = text
        start = time.time()
        self.text = model(text)
        end = time.time()
        print("Tempo de analisar texto: ", end - start, " s")
        self.entities_list = []

    def get_named_entities(self):
        for token in self.text.ents:
            if token.label_ == 'PERSON':
                start, end = self.find_position(token)
                entity = ec.Entity(text=token.text, start=start, end=end, tag='NP',
                                   pos=token.label_, type="person_unknown")
                print("Entidade do spacyNER: ", entity)
                self.entities_list.append(entity)
        return self.entities_list

    def find_position(self, token):
        start = self.input_text.find(token.text)
        end = start + len(token.text)
        return start, end
