import json


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


def query_for_instances(graph, entity_text):

    q = "select ?Entidade where {{?Entidade :Nome '{name}'}}".format(name=entity_text)
    result = graph.query(q)
    partial_results = format_result(result, "Entidade")
    return partial_results


def query_for_classes(graph, resource):

    q = "select ?Object where {{ <{nome}> rdf:type ?Object}}".format(nome=resource)
    result = graph.query(q)
    final_results = format_result(result, "Object")
    return final_results


def query_for_data_property(graph, instance, property):

    q = "select ?sobrenome where {{ <{nome}> :{prop} ?sobrenome}}".format(nome=instance, prop=property)
    r = graph.query(q)
    result = format_result(r, "sobrenome")
    if result:
        return result
    return


def query_for_object_property(graph, instance, property):

    q = "select ?pessoa2 where {{ <{pessoa1}> :{prop} ?pessoa2}}".format(pessoa1=instance, prop=property)
    r = graph.query(q)
    result = format_result(r, "pessoa2")
    if result:
        return result
    return
