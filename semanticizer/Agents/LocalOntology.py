import rdflib
import json
from semanticizer import entity_class as ec


def format_result(query_result, incognita):
    '''
    Formata o resultado, retornando lista de URIs dos resultados da query
    :param query_result:
    :param incognita:
    :return: list:
    '''
    results_list = []
    serialized = query_result.serialize(format="json")
    my_json = serialized.decode('utf8').replace("'", '"')
    # print(my_json)
    data = json.loads(my_json)

    for result in data["results"]["bindings"]:
        #print("Resultado da query: ")
        #print(result[incognita]["value"])
        if "NamedIndividual" not in str(result[incognita]["value"]): #A classe NamedIndividual do OWL2 é ignorada para o que quero
            results_list.append(result[incognita]["value"])
    return results_list


class Ontology:
    def __init__(self, ontology):
        self.ontology = ontology
        self.found_entities = []
        self.graph = rdflib.Graph()
        self.graph.parse(self.ontology, format='ttl')

    def searcher(self, chunks_list):
        '''
        Busca as entidades na ontologia e retorna um dicionario com a relação de entidades encontradas
        :param noun_chunks_list:
        :return: dict:
        '''
        for entity in chunks_list:
            instances = self.query_for_instances(entity.text)
            if instances != []:
                self.add(instances, entity)
            elif instances == []:
                is_compound = self.verify_composition(entity.text)
                if is_compound:
                    self.search_separated_instances(entity)
        return self.found_entities

    def search_separated_instances(self, entity):
        separated_text = entity.text.split(" ")
        for text in separated_text:
            instances = self.query_for_instances(text)
            if instances != []:
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
                classe = self.query_for_classes(instances[0])
                text, classe = self.verify_relationship(classe, instances[0], found_entity.text)
                found_entity = ec.Entity(text=text, start=found_entity.start, end=found_entity.end,
                                         tag='NP', pos='agg', type=classe[0])
                entity.type = classe[0]
                self.found_entities.append(found_entity)
            else:
                classe = self.query_for_classes(instances[0])
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
            extra_data = self.query_for_property(instance, "Sobrenome")
            if extra_data is not None:
                for text in extra_data:
                    if text == surname:
                        classe = self.query_for_classes(instance)
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
            classe = self.query_for_classes(instance)
            if classe not in classes:
                classes += [classe]
            extra_data = self.query_for_property(instance, "Sobrenome")
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
            people = self.query_for_property(instance, "Pessoa")
            print("Olha as pessoas: ", people)
            names = []
            texts = []
            for person in people:
                name = self.query_for_property(person, "Nome")
                names.append(name)
            for name in names:
                texts.append(name[0])
            print("Olha os nomes: ", texts)
            if len(texts) > 1:
                return texts, ['http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa']
            elif len(texts) == 1:
                return texts[0], ['http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa']
        return text, classe

    def query_for_instances(self, entity_text):
        '''
        A função retorna uma lista com as instâncias que tem o nome dado pelo texto da entidade
        :param entity_text:
        :return: list:
        '''
        q1 = "select ?Entidade where {{?Entidade :Nome '{name}'}}".format(name=entity_text)
        result1 = self.graph.query(q1)
        partial_results = format_result(result1, "Entidade")
        return partial_results

    def query_for_classes(self, resource):
        '''
        A função retorna a classe a que pertence as instâncias dadas como parâmetro
        :param entity:
        :param partial_results:
        :param g:
        :return: dict:
        '''
        q2 = "select ?Object where {{ <{nome}> rdf:type ?Object}}".format(nome=resource)
        result2 = self.graph.query(q2)
        final_results = format_result(result2, "Object")
        return final_results

    def query_for_property(self, instance, property):
        q = "select ?sobrenome where {{ <{nome}> :{prop} ?sobrenome}}".format(nome=instance, prop=property)
        r = self.graph.query(q)
        result = format_result(r, "sobrenome")
        # print("Resultado: ", result)
        if result != []:
            return result
        return

    def query_for_relationship(self, relationship):
        q = "select ?name where {{ :PESSOAL <{nome}> ?name}}".format(nome=relationship)
        r = self.graph.query(q)
        result = format_result(r, "name")
        if result != []:
            return result
        return

    @staticmethod
    def verify_composition(text):
        result = text.split(" ")
        if len(result) > 1:
            return True
        return False
