"""
@author: ricardo imagure
"""

from .POSTaggers import CogrooSemanticizer, SpacySemanticizer
# from DialogflowIntent import *
from .Agents import WatsonSkill, NLTKWordnet, LocalOntology, SpacyNER
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from semanticizer import DictionaryManager
import json
import string


class Semanticizer(object):
    sm_ontology = "db/Ontology/assistant.owl"

    def __init__(self, mode, language):
        self.mode = mode
        self.language = language
        self.watson_skill = None
        self.nltk = NLTKWordnet.NLTKWordnet()
        self.dict_manager = DictionaryManager.DictionaryManager()
        self.entities = []

    def verify_validity(self, msg):
        if self.language == 'pt':
            stop_words = set(stopwords.words('portuguese'))
        else:
            stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(msg)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        filtered_sentence = [''.join(c for c in s if c not in string.punctuation)
                             for s in filtered_sentence]
        filtered_sentence = [s for s in filtered_sentence if s]
        if filtered_sentence:
            return True
        else:
            return False

    def detect_intent(self):
        """
        Gets the intent in the WatsonAssistant response and adds it to dictionary
        :return:
        """
        intent_watson = self.watson_skill.get_intent()
        self.dict_manager.dict_add('intent', intent_watson)    ##add_intent

    def detect_datetime(self):
        """
        Gets the date/time in the WatsonAssistant response and adds it to dictionary
        :return:
        """
        datetime_entities, date_entity, hour_entity = self.watson_skill.get_date_time()
        self.dict_manager.dict_add_list(datetime_entities)
        return date_entity, hour_entity

    def semantize(self, msg):
        """
        Initializes WatsonSkill with the correct language, calls for intent recognition and
        "semantize" the message.
        :param msg:
        :return: my_json
        """
        is_valid = self.verify_validity(msg)
        if is_valid:
            if self.language == 'pt':
                self.watson_skill = WatsonSkill.WatsonSkill('pt', self.mode, msg)

            elif self.language == 'en':
                self.watson_skill = WatsonSkill.WatsonSkill('en', self.mode, msg)

            self.watson_skill.get_response()
            self.relevant_searcher(msg)

            print("Dicionário no fim das queries: ")
            print(self.dict_manager.intent_entities)

            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)

            self.dict_manager.reset()
            return my_json
        else:
            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)
            self.dict_manager.reset()
            print("Mensagem enviada não valida!")
            return my_json

    def relevant_searcher(self, msg):
        """
        Searches for the possibly relevant entities
        :param msg:
        :return:
        """
        self.detect_intent()

        date_entity, hour_entity = self.detect_datetime()

        self.run_postagger(msg)

        ontology_entities = self.semantic_memory_search()

        spacy_entities = self.spacy_NER_search(msg)

        wordnet_entities = self.wordnet_search()

        self.dict_manager.search_entities(self.entities, date_entity, hour_entity,
                                              ontology_entities, wordnet_entities, spacy_entities)

        print("\nExpressões encontradas:")
        for entity in self.entities:
            print(entity)
        print("\n" + "-" * 20)

    def run_postagger(self, msg):
        """
        Sets the correct POS Tagger and gets the entities
        :param msg:
        :return:
        """
        if self.language == 'pt':
            cogroo = CogrooSemanticizer.CogrooSemanticizer(msg)
            self.entities = cogroo.get_entities()
        elif self.language == 'en':
            spacy = SpacySemanticizer.SpacySemanticizer(msg)
            self.entities = spacy.get_entities()

    def spacy_NER_search(self, msg):
        spacy_entities = []
        # if self.language == 'pt':
        #     spacyNER = SpacyNER.SpacyNER(msg, self.language)
        #     spacy_entities = spacyNER.get_named_entities()
        #     self.dict_manager.dict_add_list(spacy_entities)
        if self.language == 'en':
            spacyNER = SpacyNER.SpacyNER(msg, self.language)
            spacy_entities = spacyNER.get_named_entities()
            self.dict_manager.verify_found_names(self.entities, spacy_entities)
            self.dict_manager.dict_add_list(spacy_entities)
        return spacy_entities

    def semantic_memory_search(self):
        """
        Searches the entities on the Semantic memory
        :return:
        """
        ontology = LocalOntology.Ontology(self.entities, self.sm_ontology)
        ontology_entities = ontology.searcher()
        self.dict_manager.verify_found_names(self.entities, ontology_entities)
        self.dict_manager.dict_add_list(ontology_entities)
        return ontology_entities

    def wordnet_search(self):
        """
        Searches the entities on the Wordnet
        :return:
        """
        if self.language == 'pt':
            wordnet_entities = self.nltk.entity_searcher(self.entities, 'por')
            self.nltk.reset()
            self.dict_manager.dict_add_list(wordnet_entities)
            return wordnet_entities
        elif self.language == 'en':
            wordnet_entities = self.nltk.entity_searcher(self.entities, 'eng')
            self.nltk.reset()
            self.dict_manager.dict_add_list(wordnet_entities)
            return wordnet_entities

