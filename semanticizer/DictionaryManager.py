import json
from semanticizer import entity_class as ec
from configs import *


class DictionaryManager:

    with open("configs/dictionary.json") as f:
        data = json.load(f)

    def __init__(self):
        self.intent_entities = self.data["SemanticClauseTemplate"]
        self.entities_history = []

    def is_same_type(self, type1, type2):
        if type1 in self.data["SourceTags"]["person_known_tags"] \
                and type2 in self.data["SourceTags"]["person_known_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["person_unknown_tags"] \
                and type2 in self.data["SourceTags"]["person_unknown_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["person_known_tags"] \
                and type2 in self.data["SourceTags"]["person_unknown_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["person_known_tags"] \
                and type2 in self.data["SourceTags"]["place_unknown_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["person_unknown_tags"] \
                and type2 in self.data["SourceTags"]["place_unknown_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["place_known_tags"] \
                and type2 in self.data["SourceTags"]["place_known_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["place_unknown_tags"] \
                and type2 in self.data["SourceTags"]["place_unknown_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["commitment_tags"] \
                and type2 in self.data["SourceTags"]["commitment_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["hour_tags"] \
                and type2 in self.data["SourceTags"]["hour_tags"]:
            return True
        elif type1 in self.data["SourceTags"]["date_tags"] \
                and type2 in self.data["SourceTags"]["date_tags"]:
            return True
        return False

    def is_repeated(self, new_entity):
        for entity in self.entities_history:
            if ec.exists_overlap(entity, new_entity) and self.is_same_type(entity.type, new_entity.type):
                return True
        self.entities_history.append(new_entity)
        return False

    def dict_add_list(self, entities_list):
        for entity in entities_list:
            if not self.is_repeated(entity):
                self.dict_add(entity.type, entity.text)

    def dict_add(self, index, value):
        list_value = [value]
        exists = False
        for item in self.data["SourceTags"].values():
            if index in item:
                exists = True
        if not exists:
            index = self.data["DefinitiveTags"]["dont_know_tag"]

        else:
            if index in self.data["SourceTags"]["person_known_tags"]:
                index = self.data["DefinitiveTags"]["person_known_tag"]

            elif index in self.data["SourceTags"]["person_unknown_tags"]:
                index = self.data["DefinitiveTags"]["person_unknown_tag"]

            elif index in self.data["SourceTags"]["place_known_tags"]:
                index = self.data["DefinitiveTags"]["place_known_tag"]

            elif index in self.data["SourceTags"]["place_unknown_tags"]:
                index = self.data["DefinitiveTags"]["place_unknown_tag"]

            elif index in self.data["SourceTags"]["intent_tags"]:
                index = self.data["DefinitiveTags"]["intent_tag"]

            elif index in self.data["SourceTags"]["commitment_tags"]:
                index = self.data["DefinitiveTags"]["commitment_tag"]

            elif index in self.data["SourceTags"]["date_tags"]:
                index = self.data["DefinitiveTags"]["date_tag"]

            elif index in self.data["SourceTags"]["hour_tags"]:
                index = self.data["DefinitiveTags"]["hour_tag"]

        if self.intent_entities[index] != list_value:
                self.intent_entities[index] += list_value
        else:
            self.intent_entities[index] = list_value

    def reset(self):
        for index in self.intent_entities:
            self.intent_entities[index] = []
            self.entities_history = []

    def search_entities(self, all_entities, date_entities, hour_entities, ontology_entities, wordnet_entities,
                        spacy_entities):

        for entity in all_entities:
            existence = False

            if date_entities:
                for date_entity in date_entities:
                    if ec.exists_overlap(entity, date_entity):
                        existence = True
            if hour_entities:
                for hour_entity in hour_entities:
                    if ec.exists_overlap(entity, hour_entity):
                        existence = True
            if ontology_entities:
                for ontology_entity in ontology_entities:
                    if ec.exists_overlap(entity, ontology_entity):
                        existence = True
            if wordnet_entities:
                for wordnet_entity in wordnet_entities:
                    if ec.exists_overlap(entity, wordnet_entity):
                        existence = True
            if spacy_entities:
                for spacy_entity in spacy_entities:
                    if ec.exists_overlap(entity, spacy_entity):
                        existence = True

            if not existence and (entity.pos in self.data["SourceTags"]["person_unknown_tags"]):
                self.dict_add(entity.pos, entity.text)

            elif not existence:
                self.add_dont_know(entity)

    def add_dont_know(self, entity):
        print("Existance é falsa, entidade: ", entity.text)
        if entity.pos == 'prop':
            self.dict_add(self.data["DefinitiveTags"]["person_unknown_tag"], entity.text)
        else:
            self.dict_add(self.data["DefinitiveTags"]["dont_know_tag"], entity.text)
