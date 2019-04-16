from nltk.corpus import wordnet
from semanticizer import entity_class as ec
import time


class NLTKWordnet(object):

    def __init__(self, synsets):
        self.found_entities = []
        self.synsets_list = synsets.synsets_list

    def reset(self):
        self.found_entities = []

    def entity_searcher(self, entities, language):
        for entity in entities:
            if self.is_compound(entity.text):
                self.separate_and_search(entity, language)
            else:
                self.search_word(entity, language)
        return self.found_entities

    def separate_and_search(self, entity, language):
        separated_text = entity.text.split(" ")
        for text in separated_text:
            partial_entity = ec.Entity(text=text, start=entity.start, end=entity.end,
                                             tag=entity.tag, pos=entity.pos)
            self.search_word(partial_entity, language, entity)

    def search_word(self, entity, language, compound_entity=None):
        word = entity.text
        wn = wordnet.synsets(word, pos='n', lang=language)
        if wn != []:
            qtd = 0
            start = time.time()
            for synset in self.synsets_list:
                for item in wn:
                    similarity = item.path_similarity(synset)
                    qtd += 1
                    if similarity > 0.4:
                        print("\n"+"Similaridades encontradas na WordNet")
                        print("Texto: ", entity.text, "-", item, "-", synset.name(), "similaridade: ", similarity)
                        if compound_entity:
                            found_entity = ec.Entity(text=word, start=entity.start, end=entity.end,
                                                     tag=entity.tag, pos=entity.pos, type=synset.name())
                        else:
                            found_entity = ec.Entity(text=word, start=entity.start, end=entity.end,
                                                     tag=entity.tag, pos=entity.pos, type=synset.name())
                        self.found_entities.append(found_entity)
            end = time.time()
            print("--> Quantidade de comparações: ", qtd)
            print("--> Tempo para comparar synsets: ", end-start, " s")

    @staticmethod
    def is_compound(text):
        result = text.split(" ")
        if len(result) > 1:
            return True
        return False
