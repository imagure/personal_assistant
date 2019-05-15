from semanticizer.Semanticizer import *
from semanticizer.Agents.initializer import Initializer
from ModeManager import *

sm_ontology = "db/Ontology/assistant.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()


def main():
    print('Por favor, diga a língua para o sistema ("pt" ou "en")')
    print('> ')
    language = input()
    dict_output = {'mode': 'response'}
    json_output = json.loads(json.dumps(dict_output))
    mode_manager = ModeManager()
    mode = mode_manager.which_mode(json.dumps(json_output, indent=4, sort_keys=True))
    file = open("tests/tests_phrases/phrases.txt", mode="r")
    semanticizer = Semanticizer(mode, initial_vars, 1, language)

    for line in file:
        semanticizer.dict_manager.reset()
        print(semanticizer.validate_and_semantize(line))


if __name__ == '__main__':
    main()
