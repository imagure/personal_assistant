import rdflib
from db.Ontology.ontology_interface import *

sm_ontology = "db/Ontology/assistant.owl"
text = "Ricardo"
text2 = "Imagure"

graph = rdflib.Graph()

graph.parse(sm_ontology, format='ttl')

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
