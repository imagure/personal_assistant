import rdflib
from db.Ontology.ontology_interface import *

sm_ontology = "db/Ontology/assistant.owl"

graph = rdflib.Graph()

graph.parse(sm_ontology, format='ttl')

pessoa = query_for_instances(graph, "Edna")

print("instance: ", pessoa)

contatos = query_for_object_property(graph, pessoa[0], "contato")

print("object property: ", contatos)

nomes_contatos = []
for pessoa in contatos:
    nome = query_for_data_property(graph, pessoa, "Nome")
    nomes_contatos.append(nome)
print(nomes_contatos)
