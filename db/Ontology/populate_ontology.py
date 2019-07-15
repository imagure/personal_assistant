from db.Ontology.ontology_interface import *
from semanticizer.Agents.initializer import Initializer

# ricardo.imagure:                    1   DHCH9G02U
# Ricardo Imagure/ricardo.imagure092: 2   DHHBT90B0
# Mateus Ramos Vendramini:            3   CKAJF4JSK(temp)

ricardo_imagure = {"first_name": "Ricardo",
                   "last_name": "Imagure"}

ricardo_camargo = {"first_name": "Ricardo",
                   "last_name": "Camargo"}

mateus_vendramini = {"first_name": "Mateus",
                     "last_name": "Vendramini"}

sm_ontology = "db/Ontology/assistant_test.owl"
initial_vars = Initializer()
initial_vars.set_ontology(sm_ontology)

insert_new_user(initial_vars.graph, ricardo_imagure, 1)
insert_new_user(initial_vars.graph, ricardo_camargo, 2)
insert_new_user(initial_vars.graph, mateus_vendramini, 3)

insert_contacts(initial_vars.graph, 1, [2, 3])
insert_contacts(initial_vars.graph, 2, [1, 3])
insert_contacts(initial_vars.graph, 3, [1, 2])
