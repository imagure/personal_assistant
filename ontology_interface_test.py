import rdflib
from db.Ontology.ontology_interface import *

sm_ontology = "db/Ontology/assistant.owl"
text = "Ricardo"
text2 = "Imagure"

graph = rdflib.Graph()

graph.parse(sm_ontology, format='ttl')

insert_new_user(graph, 'joao', user_id=10)

pessoa = query_for_id(graph, 10)

print("Pessoa adicionada: ", pessoa)

nome = query_for_data_property(graph, pessoa[0], "Nome")

print("Nome da pessoa: ", nome)

insert_contacts(graph, user_id=10, contacts=[1, 2, 3, 4])

contatos = query_for_object_property(graph, pessoa[0], "contato")

print("object property: ", contatos)

"""
relationships = query_for_instances(graph, 'http://www.semanticweb.org/ricardo/ontologies/2019/1/assistant#Relacionamento')

print("\n Relationships do user: ", relationships)

pessoa = query_for_id(graph, 1)

print("instance: ", pessoa)

contatos = query_for_object_property(graph, pessoa[0], "contato")

print("object property: ", contatos)

nomes_contatos = []
sobrenomes_contatos = []
contatos_encontrados = []
pessoa_encontrada = []

for pessoa in contatos:
    nomes = query_for_data_property(graph, pessoa, "Nome")
    if text in nomes:
        contatos_encontrados.append(pessoa)
    nomes_contatos.append(nomes)
print(nomes_contatos)
if len(contatos_encontrados) > 1:
    # if is_compound(text):
    #   try_disambiguate(text)
    for pessoa in contatos_encontrados:
        sobrenomes = query_for_data_property(graph, pessoa, "Sobrenome")
        if text2 in sobrenomes:
            pessoa_encontrada.append(pessoa)
    # else:
    #   add_conflict(text)

# if len(pessoa_encontrada) > 1:
    # add_conflict()
# else:
print(pessoa_encontrada)

id_contato = query_for_data_property(graph, pessoa_encontrada[0], "id")

print(id_contato)
"""