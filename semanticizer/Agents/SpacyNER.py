import spacy
from semanticizer import entity_class as ec


class SpacyNER(object):

    def __init__(self, text, model):
        self.input_text = text
        self.text = model(text)
        self.entities_list = []

    def get_named_entities(self):
        print("-" * 20, "> SpacyNER")
        for token in self.text.ents:
            if token.label_ == 'PERSON':
                start, end = self.find_position(token)
                entity = ec.Entity(text=token.text, start=start, end=end, tag='NP',
                                   pos=token.label_, type="person_unknown")
                self.entities_list.append(entity)

        for entity in self.entities_list:
            print(entity)

        return self.entities_list

    def find_position(self, token):
        start = self.input_text.find(token.text)
        end = start + len(token.text)
        return start, end
