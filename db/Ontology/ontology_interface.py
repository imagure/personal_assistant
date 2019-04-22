import json


def format_result(query_result, incognita):

    results_list = []
    serialized = query_result.serialize(format="json")
    my_json = serialized.decode('utf8').replace("'", '"')
    data = json.loads(my_json)

    for result in data["results"]["bindings"]:
        if "NamedIndividual" not in str(result[incognita]["value"]): #A classe NamedIndividual do OWL2 é ignorada para o que quero
            results_list.append(result[incognita]["value"])
    return results_list


def query_for_instances(graph, entity_text):

    q1 = "select ?Entidade where {{?Entidade :Nome '{name}'}}".format(name=entity_text)
    result1 = graph.query(q1)
    partial_results = format_result(result1, "Entidade")
    return partial_results


def query_for_classes(graph, resource):

    q2 = "select ?Object where {{ <{nome}> rdf:type ?Object}}".format(nome=resource)
    result2 = graph.query(q2)
    final_results = format_result(result2, "Object")
    return final_results


def query_for_property(graph, instance, property):

    q = "select ?sobrenome where {{ <{nome}> :{prop} ?sobrenome}}".format(nome=instance, prop=property)
    r = graph.query(q)
    result = format_result(r, "sobrenome")
    if result != []:
        return result
    return


def query_for_relationship(graph, relationship):

    q = "select ?name where {{ :PESSOAL <{nome}> ?name}}".format(nome=relationship)
    r = graph.query(q)
    result = format_result(r, "name")
    if result != []:
        return result
    return
