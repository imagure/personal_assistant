from semanticizer import entity_class as ec
from db.Ontology.ontology_interface import *


class Ontology:
    def __init__(self, graph):
        self.found_entities = []
        self.graph = graph

    def reset_entities(self):
        self.found_entities = []

    def searcher(self, chunks_list):
        '''
        Busca as entidades na ontologia e retorna um dicionario com a relação de entidades encontradas
        :param noun_chunks_list:
        :return: dict:
        '''
        for entity in chunks_list:
            instances = query_for_instances(self.graph, entity.text)
            if instances:
                self.add(instances, entity)
            elif not instances:
                is_compound = self.verify_composition(entity.text)
                if is_compound:
                    self.search_separated_instances(entity)

        print("\n", "-" * 20, "> LocalOntology")
        for entity in self.found_entities:
            print(entity)

        return self.found_entities

    def search_separated_instances(self, entity):
        separated_text = entity.text.split(" ")
        for text in separated_text:
            instances = query_for_instances(self.graph, text)
            if instances:
                new_start, new_end = ec.find_new_location(entity, text)
                found_entity = ec.Entity(text=text, start=new_start, end=new_end,
                                         tag='NP', pos='agg')
                self.add(instances, entity, found_entity, test_ambiguous=True)

    def add(self, instances, entity, found_entity=None, test_ambiguous=False):
        """
        Adiciona termos ao dicionário, individuais, em conflito, ou busca ambiguidade
        :param instances:
        :param text:
        :param test_ambiguous:
        :return:
        """
        number_of_results = len(instances)
        if number_of_results == 1:
            if found_entity:
                classe = query_for_classes(self.graph, instances[0])
                text, classe = self.verify_relationship(classe, instances[0], found_entity.text)
                found_entity = ec.Entity(text=text, start=found_entity.start, end=found_entity.end,
                                         tag='NP', pos='agg', type=classe[0])
                entity.type = classe[0]
                self.found_entities.append(found_entity)
            else:
                classe = query_for_classes(self.graph, instances[0])
                text, classe = self.verify_relationship(classe, instances[0], entity.text)
                found_entity = ec.Entity(text=text, start=entity.start, end=entity.end,
                                         tag='NP', pos='agg', type=classe[0])
                entity.type = classe[0]
                self.found_entities.append(found_entity)
        elif number_of_results > 1 and not test_ambiguous:
            self.conflict(instances, entity)
        elif number_of_results > 1 and test_ambiguous:
            ambiguous = self.disambiguate(instances, entity)
            if not ambiguous:
                self.conflict(instances, entity, found_entity)

    def disambiguate(self, instances, entity):
        text = entity.text.split(" ")
        name = text[0].strip()
        surname = text[1].strip()
        for instance in instances:
            extra_data = query_for_property(self.graph, instance, "Sobrenome")
            if extra_data is not None:
                for text in extra_data:
                    if text == surname:
                        classe = query_for_classes(self.graph, instance)
                        vect = name + ' ' + surname
                        found_entity = ec.Entity(text=vect, start=entity.start, end=entity.end,
                                                 tag='NP', pos='agg', type=classe[0])
                        self.found_entities.append(found_entity)
                        return True
        return False

    def conflict(self, instances, entity, found_entity=None):
        vect = []
        classes = []
        if found_entity:
            text = found_entity.text
            start = found_entity.start
            end = found_entity.end
        else:
            text = entity.text
            start = entity.start
            end = entity.end
        for instance in instances:
            classe = query_for_classes(self.graph, instance)
            if classe not in classes:
                classes += [classe]
            extra_data = query_for_property(self.graph, instance, "Sobrenome")
            if extra_data is not None:
                vect += [text + ' ' + extra_data[0]]
            else:
                vect += [text]
        for classe in classes:
            found_entity = ec.Entity(text=vect, start=start, end=end,
                                     tag='NP', pos='agg', type=classe[0])
            self.found_entities.append(found_entity)

    def verify_relationship(self, classe, instance, text):
        if classe[0] == 'http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Relacionamento':
            people = query_for_property(self.graph, instance, "Pessoa")
            names = []
            texts = []
            for person in people:
                name = query_for_property(self.graph, person, "Nome")
                names.append(name)
            for name in names:
                texts.append(name[0])
            if len(texts) > 1:
                return texts, ['http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa']
            elif len(texts) == 1:
                return texts[0], ['http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa']
        return text, classe

    @staticmethod
    def verify_composition(text):
        result = text.split(" ")
        if len(result) > 1:
            return True
        return False
