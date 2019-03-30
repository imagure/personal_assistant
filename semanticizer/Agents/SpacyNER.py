import spacy
from semanticizer import entity_class as ec


class SpacyNER(object):

    def __init__(self, text, language):
        self.input_text = text
        self.language = language
        self.nlp = self.set_model()
        self.text = self.nlp(text)
        self.entities_list = []

    def set_model(self):
        # if self.language == 'pt':
        #     return spacy.load('pt_core_news_sm')
        if self.language == 'en':
            return spacy.load('en_core_web_sm')

    def get_named_entities(self):
        for token in self.text.ents:
            if token.label_ == 'PERSON':
                start, end = self.find_position(token)
                entity = ec.Entity(text=token.text, start=start, end=end, tag='NP',
                                   pos=token.label_, type="person_unknown")
                print("Aqui está a entidade do spacyNER: ", entity)
                self.entities_list.append(entity)
        return self.entities_list

    def find_position(self, token):
        start = self.input_text.find(token.text)
        end = start + len(token.text)
        return start, end
