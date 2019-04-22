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
import time


class Semanticizer(object):

    def __init__(self, mode, language, initial_vars):
        self.mode = mode
        self.language = language
        self.watson_skill = None
        self.initial_vars = initial_vars
        self.nltk = NLTKWordnet.NLTKWordnet(initial_vars)
        self.ontology = LocalOntology.Ontology(initial_vars.graph)
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
        start_total = time.time()
        is_valid = self.verify_validity(msg)
        if is_valid:
            start = time.time()
            if self.language == 'pt':
                self.watson_skill = WatsonSkill.WatsonSkill('pt', self.mode, msg)

            elif self.language == 'en':
                self.watson_skill = WatsonSkill.WatsonSkill('en', self.mode, msg)

            self.watson_skill.get_response()
            end = time.time()
            print("--> Tempo de buscar resposta do Watson: ", end - start, " s")

            self.relevant_searcher(msg)

            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)

            self.dict_manager.reset()
            end = time.time()
            print("\n--> Tempo total do semantizador: ", end-start_total, " s")
            return my_json
        else:
            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)
            self.dict_manager.reset()
            end = time.time()
            print("Mensagem enviada não valida!")
            print("\n--> Tempo total do semantizador: ", end-start_total, " s")
            return my_json

    def relevant_searcher(self, msg):
        """
        Searches for the possibly relevant entities
        :param msg:
        :return:
        """
        self.detect_intent()

        date_entity, hour_entity = self.detect_datetime()

        start = time.time()
        self.run_postagger(msg)
        end = time.time()
        print("--> Tempo do postagger: ", end - start, " s")

        start = time.time()
        ontology_entities = self.semantic_memory_search()
        end = time.time()
        print("--> Tempo da memória semântica: ", end - start, " s")

        start = time.time()
        spacy_entities = self.spacy_NER_search(msg)
        end = time.time()
        print("--> Tempo do spacyNER: ", end - start, " s")

        start = time.time()
        wordnet_entities = self.wordnet_search()
        end = time.time()
        print("--> Tempo da Wordnet: ", end - start, " s")

        self.dict_manager.search_entities(self.entities, date_entity, hour_entity,
                                              ontology_entities, wordnet_entities, spacy_entities)

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
            model = self.initial_vars.spacy_en
            spacy = SpacySemanticizer.SpacySemanticizer(msg, model)
            self.entities = spacy.get_entities()

    def spacy_NER_search(self, msg):
        spacy_entities = []
        # if self.language == 'pt':
        #     spacyNER = SpacyNER.SpacyNER(msg, self.language)
        #     spacy_entities = spacyNER.get_named_entities()
        #     self.dict_manager.dict_add_list(spacy_entities)
        if self.language == 'en':
            model = self.initial_vars.spacy_en
            spacyNER = SpacyNER.SpacyNER(msg, model)
            spacy_entities = spacyNER.get_named_entities()
            self.dict_manager.dict_add_list(spacy_entities)
        return spacy_entities

    def semantic_memory_search(self):
        """
        Searches the entities on the Semantic memory
        :return:
        """
        ontology_entities = self.ontology.searcher(self.entities)
        self.ontology.reset_entities()
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

