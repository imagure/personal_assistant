import json
from rdflib.namespace import RDF
from rdflib import URIRef, Literal


def format_result(query_result, keyword):

    results_list = []
    serialized = query_result.serialize(format="json")
    my_json = serialized.decode('utf8').replace("'", '"')
    data = json.loads(my_json)

    for result in data["results"]["bindings"]:
        # A classe 'NamedIndividual' do OWL2 é ignorada para o que quero
        if "NamedIndividual" not in str(result[keyword]["value"]):
            results_list.append(result[keyword]["value"])
    return results_list


def query_by_id(graph, user_id):

    q = "select ?Usuario where {{?Usuario :id {user_id}}}".format(user_id=user_id)
    result = graph.query(q)
    partial_results = format_result(result, "Usuario")
    return partial_results


def query_for_instances(graph, entity_text):

    q = "select ?Entidade where {{?Entidade rdf:type <{name}>}}".format(name=entity_text)
    result = graph.query(q)
    partial_results = format_result(result, "Entidade")
    return partial_results


def query_for_classes(graph, resource):

    q = "select ?Object where {{ <{nome}> rdf:type ?Object}}".format(nome=resource)
    result = graph.query(q)
    final_results = format_result(result, "Object")
    return final_results


def query_for_data_property(graph, instance, property):

    q = "select ?property where {{ <{nome}> :{prop} ?property}}".format(nome=instance, prop=property)
    r = graph.query(q)
    result = format_result(r, "property")
    if result:
        return result
    return


def query_for_object_property(graph, instance, property):

    q = "select ?pessoa2 where {{ <{pessoa1}> :{prop} ?pessoa2}}".format(pessoa1=instance, prop=property)
    r = graph.query(q)
    result = format_result(r, "pessoa2")
    return result


def query_for_user_id(graph, instance):

    q = "select ?user_id where {{ <{pessoa}> :id ?user_id}}".format(pessoa=instance)
    r = graph.query(q)
    result = format_result(r, "user_id")
    if result:
        return result[0]
    return


def insert_new_user(graph, user_name, user_id):
    first_name = Literal(user_name["first_name"])
    last_name = Literal(user_name["last_name"])
    user_sm_id = Literal(user_id)

    user_uri = "http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa{}".format(user_id)
    user = URIRef(user_uri)

    pessoa = URIRef("http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Pessoa")
    name = URIRef("http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Nome")
    surname = URIRef("http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Sobrenome")
    sm_id = URIRef("http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#id")

    graph.add((user, RDF.type, pessoa))
    graph.add((user, name, first_name))
    graph.add((user, surname, last_name))
    graph.add((user, sm_id, user_sm_id))

    graph.serialize(destination='db/Ontology/assistant_test.owl', format='ttl')


def insert_contacts(graph, user_id, contacts):

    user = URIRef(query_by_id(graph, user_id)[0])
    contato = URIRef("http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#contato")
    for contact in contacts:
        user_contact = query_by_id(graph, contact)
        if user_contact:
            user_contact_uri = URIRef(user_contact[0])
            graph.add((user, contato, user_contact_uri))
            graph.add((user_contact_uri, contato, user))

    graph.serialize(destination='db/Ontology/assistant_test.owl', format='ttl')
