from semanticizer.Semanticizer import *
from ModeManager import *
from dialog_message.dialog_message import *
from dialog_manager.dialog_manager import DialogManager
from output_generator.OutputGenerator import *
import json
import time
from semanticizer.Agents.initializer import Initializer

sm_ontology = "db/Ontology/assistant.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()


def execute_semanticizer(semanticizer, line):
    semanticizer.dict_manager.reset()
    my_json = semanticizer.semantize(line)
    print("JSON: ")
    print(my_json)
    return my_json


def main():
    # print('Por favor, escreva abaixo um texto (Ex: Quero marcar uma conversa com o Mateus no domingo /'
    #     ' I want to schedule a meeting with Adam the next week) \n')
    print('Por favor, diga a língua para o sistema ("pt" ou "en")')
    print('> ')
    language = input()
    dict_output = {'mode': 'response'}
    json_output = json.loads(json.dumps(dict_output))
    mode_manager = ModeManager()
    mode = mode_manager.which_mode(json.dumps(json_output, indent=4, sort_keys=True))
    file = open("tests/tests_phrases/frases_teste.txt", mode="r")

    semanticizer = Semanticizer(mode, language, initial_vars)
    dm = DialogManager()
    dm.start()
    og = OutputGenerator()
    og.start()

    for line in file:
        print("\n" + "=" * 50)
        print("O texto é: ", line)
        print("\nA língua do documento é: ", language)
        my_json = execute_semanticizer(semanticizer, line)
        message = DialogMessage.from_json(my_json)
        message.id_user = 1
        dm.dispatch_msg(message)


if __name__ == '__main__':
    main()
