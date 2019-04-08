# import subprocess
from semanticizer.Semanticizer import *
import json
from ModeManager import *
from dialog_message import *
# from dialog_manager import *


def execute_semanticizer(semanticizer, line):
    semanticizer.dict_manager.reset()
    my_json = semanticizer.semantize(line)
    print("JSON: ")
    print(my_json)
    return my_json


def main():
    # subprocess.call(['java', '-jar', '/home/ricardo/Documents/Assistente_Pessoal/cogroo4py/cogroo4py.jar'])
    # print('Por favor, escreva abaixo um texto (Ex: Quero marcar uma conversa com o Mateus no domingo /'
    #     ' I want to schedule a meeting with Adam the next week) \n')
    print('Por favor, diga a língua para o sistema ("pt" ou "en")')
    print('> ')
    language = input()
    dict_output = {'mode': 'response'}
    json_output = json.loads(json.dumps(dict_output))
    mode_manager = ModeManager()
    mode = mode_manager.which_mode(json.dumps(json_output, indent=4, sort_keys=True))
    file = open("resources/frases_teste.txt", mode="r")

    semanticizer = Semanticizer(mode, language)
    for line in file:
        print("\n" + "=" * 50)
        print("O texto é: ", line)
        print("\nA língua do documento é: ", language)
        execute_semanticizer(semanticizer, line)


if __name__ == '__main__':
    main()
