# import subprocess
from semanticizer.Semanticizer import *
#import json
# from ModeManager import *
from dialog_message.dialog_message import *
from dialog_manager.dialog_manager import DialogManager


def main():
    # subprocess.call(['java', '-jar', '/home/ricardo/Documents/Assistente_Pessoal/cogroo4py/cogroo4py.jar'])
    # print('Por favor, escreva abaixo um texto (Ex: Quero marcar uma conversa com o Mateus no domingo /'
    #     ' I want to schedule a meeting with Adam the next week) \n')
    print('Por favor, diga a língua para o sistema ("pt" ou "en")')
    print('> ')
    language = input()
    dict_output = {'mode': 'regular'}
    json_output = json.loads(json.dumps(dict_output))  # Clausula semântica (json) do OutputGenerator para o Semantizador
    # mode_manager = ModeManager()
    # mode = mode_manager.which_mode(json.dumps(json_output, indent=4, sort_keys=True))
    file = open("resources/frases_teste.txt", mode="r")
    dm = DialogManager()
    dm.start()
    semanticizer = Semanticizer('regular', language)
    #for line in file:  # testes em frases pre-escritas
    while True:
            print("Digite a frase")
            line = input()
            semanticizer.intent_entities = {}
            my_json = semanticizer.semantize(line)
            print("JSON: ")
            print(my_json)
            message = DialogMessage.from_json((my_json))
            message.id_user = 1
            print("with_list%s\nintent%s\ndate%s\nhour%s\nplace%s" % (message.with_list, message.intent, message.date, message.hour, message.place))
            dm.dispatch_msg(message)


if __name__ == '__main__':
    main()
