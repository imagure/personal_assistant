"""
@author: ricardo imagure
"""

import json
import string
import time

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from semanticizer import DictionaryManager
from .Agents import WatsonSkill, NLTKWordnet, LocalOntology, SpacyNER
from .POSTaggers import CogrooSemanticizer, SpacySemanticizer


class Semanticizer(object):

    def __init__(self, mode, initial_vars, user_id, language=None):
        self.mode = mode
        self.user_id = user_id
        self.language = language
        self.watson_skill = None
        self.initial_vars = initial_vars
        self.nltk = NLTKWordnet.NLTKWordnet(initial_vars)
        self.ontology = LocalOntology.Ontology(initial_vars.graph)
        self.dict_manager = DictionaryManager.DictionaryManager()
        self.entities = []

    def set_language(self, language):

        self.language = language

    def validate_and_semantize(self, msg):

        print("=" * 20, "> .semantize begin")
        print("texto recebido: ", msg)
        print("língua do semantizador: ", self.language)

        is_valid = self._verify_validity(msg)

        if is_valid:

            self._relevant_entities_searcher(msg)

            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)
            self.dict_manager.reset()

            return my_json
        else:
            my_json = json.dumps(self.dict_manager.intent_entities, indent=4, ensure_ascii=False)
            self.dict_manager.reset()

            print("Mensagem enviada não valida!")
            print("=" * 20, "> .semantize end")
            return my_json

    def _relevant_entities_searcher(self, msg):
        """
        Run all of the Agents in sequence and adds the entities to the dict_manager dictionary
        :param msg:
        :return:
        """

        start_total = time.time()

        start = time.time()
        self.watson_skill = WatsonSkill.WatsonSkill(self.language, self.mode, msg)
        self.watson_skill.get_response()
        end = time.time()
        print("\n--> Tempo de buscar resposta do Watson: ", end - start, " s")

        start = time.time()
        self._detect_intent()
        date_entity, hour_entity = self._detect_datetime()
        end = time.time()
        print("--> Tempo do Watson : ", end - start, " s")

        start = time.time()
        self._run_postagger(msg)
        end = time.time()
        print("--> Tempo do PosTagger: ", end - start, " s")

        start = time.time()
        ontology_entities = self._semantic_memory_search()
        end = time.time()
        print("--> Tempo do LocalOntology: ", end - start, " s")

        start = time.time()
        spacy_entities = self._spacy_NER_search(msg)
        end = time.time()
        print("--> Tempo do SpacyNER: ", end - start, " s")

        start = time.time()
        wordnet_entities = self._wordnet_search()
        end = time.time()
        print("--> Tempo da Wordnet: ", end - start, " s")

        self.dict_manager.search_entities(self.entities, date_entity, hour_entity,
                                          ontology_entities, wordnet_entities, spacy_entities)

        print("\n", "-" * 20, "> Output")
        print(self.dict_manager.intent_entities)

        end = time.time()
        print("\n--> Tempo Total do semantizador: ", end - start_total, " s")
        print("=" * 20, "> .semantize end")

    def _verify_validity(self, msg):
        if self.language == 'pt':
            stop_words = set(stopwords.words('portuguese'))
            stop_words.remove("não")
        else:
            stop_words = set(stopwords.words('english'))
            stop_words.remove("no")
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

    def _detect_intent(self):
        """
        Gets the intent in the WatsonAssistant response and adds it to dictionary
        :return:
        """
        intent_watson = self.watson_skill.get_intent()
        self.dict_manager.dict_add('intent', intent_watson, origin="Watson")

    def _detect_datetime(self):
        """
        Gets the date/time in the WatsonAssistant response and adds it to dictionary
        :return:
        """
        datetime_entities, date_entity, hour_entity = self.watson_skill.get_date_time()
        self.dict_manager.dict_add_list(datetime_entities, origin="Watson")
        return date_entity, hour_entity

    def _run_postagger(self, msg):
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

    def _spacy_NER_search(self, msg):
        spacy_entities = []
        # spaCy em português não adicionou melhora sensível e deixou a aplicação mais pesada
        # if self.language == 'pt':
        #     spacyNER = SpacyNER.SpacyNER(msg, self.language)
        #     spacy_entities = spacyNER.get_named_entities()
        #     self.dict_manager.dict_add_list(spacy_entities, origin="spacyNER")
        if self.language == 'en':
            model = self.initial_vars.spacy_en
            spacyNER = SpacyNER.SpacyNER(msg, model)
            spacy_entities = spacyNER.get_named_entities()
            self.dict_manager.dict_add_list(spacy_entities, origin="spacyNER")
        return spacy_entities

    def _semantic_memory_search(self):
        """
        Searches the entities on the Semantic memory
        :return:
        """
        ontology_entities = self.ontology.searcher(self.entities, self.user_id)
        self.ontology.reset_entities()
        self.dict_manager.dict_add_list(ontology_entities, origin="LocalOntology")
        return ontology_entities

    def _wordnet_search(self):
        """
        Searches the entities on the Wordnet
        :return:
        """
        self.nltk.set_language(self.language)
        wordnet_entities = self.nltk.entity_searcher(self.entities)
        self.nltk.reset()
        self.dict_manager.dict_add_list(wordnet_entities, origin="WordNet")
        return wordnet_entities
