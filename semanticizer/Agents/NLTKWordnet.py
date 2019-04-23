from nltk.corpus import wordnet
from semanticizer import entity_class as ec
from nltk.corpus import wordnet_ic
# import time

brown_ic = wordnet_ic.ic('ic-brown.dat')


class NLTKWordnet(object):

    def __init__(self, synsets):
        self.found_entities = []
        self.place_synsets_list = synsets.place_synsets_list
        self.commitment_synsets_list = synsets.commitment_synsets_list
        self.people_synsets_list = synsets.people_synsets_list

    def reset(self):
        self.found_entities = []

    def entity_searcher(self, entities, language):
        for entity in entities:
            if self.is_compound(entity.text):
                self.separate_and_search(entity, language)
            else:
                self.search_word(entity, language)

        print("\n", "-" * 20, "> NLTKWordnet")
        for entity in self.found_entities:
            print(entity)

        return self.found_entities

    def separate_and_search(self, entity, language):
        separated_text = entity.text.split(" ")
        for text in separated_text:
            new_start, new_end = ec.find_new_location(entity, text)
            partial_entity = ec.Entity(text=text, start=new_start, end=new_end,
                                             tag=entity.tag, pos=entity.pos, type=entity.type)
            self.search_word(partial_entity, language)

    def search_word(self, entity, language):
        word = entity.text
        wn = wordnet.synsets(word, pos='n', lang=language)
        if wn:
            qtd = 0
            # start = time.time()
            place_similarity = 0
            commitment_similarity = 0
            people_similarity = 0
            for synset in self.place_synsets_list:
                for item in wn:
                    similarity = item.jcn_similarity(synset, ic=brown_ic)
                    # if similarity > 0.12:
                    #     print("Similaridade entre ", item, " e ", synset, " = ", similarity)
                    qtd += 1
                    if similarity > place_similarity:
                        place_similarity = similarity
            for synset in self.commitment_synsets_list:
                for item in wn:
                    similarity = item.jcn_similarity(synset, ic=brown_ic)
                    # if similarity > 0.12:
                    #     print("Similaridade entre ", item, " e ", synset, " = ", similarity)
                    qtd += 1
                    if similarity > commitment_similarity:
                        commitment_similarity = similarity

            for synset in self.people_synsets_list:
                for item in wn:
                    similarity = item.jcn_similarity(synset, ic=brown_ic)
                    # if similarity > 0.12:
                    #     print("Similaridade entre ", item, " e ", synset, " = ", similarity)
                    qtd += 1
                    if similarity > people_similarity:
                        people_similarity = similarity

            if place_similarity > commitment_similarity and place_similarity > commitment_similarity \
                    and place_similarity > 0.12:
                found_entity = ec.Entity(text=word, start=entity.start, end=entity.end,
                                         tag=entity.tag, pos=entity.pos, type="place_unknown")
                self.found_entities.append(found_entity)

            elif commitment_similarity > place_similarity and commitment_similarity > people_similarity \
                    and commitment_similarity > 0.12:
                found_entity = ec.Entity(text=word, start=entity.start, end=entity.end,
                                         tag=entity.tag, pos=entity.pos, type="commitment")
                self.found_entities.append(found_entity)

            elif people_similarity > place_similarity and people_similarity > commitment_similarity \
                    and people_similarity > 0.12:
                found_entity = ec.Entity(text=word, start=entity.start, end=entity.end,
                                         tag=entity.tag, pos=entity.pos, type="person_unknown")
                self.found_entities.append(found_entity)

            # end = time.time()
            # print("--> Quantidade de comparações: ", qtd)
            # print("--> Tempo para comparar synsets: ", end-start, " s")

    @staticmethod
    def is_compound(text):
        result = text.split(" ")
        if len(result) > 1:
            return True
        return False
