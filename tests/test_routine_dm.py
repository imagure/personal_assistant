from semanticizer.Semanticizer import *
from dialog_message.dialog_message import *
from dialog_manager.dialog_manager import DialogManager
from semanticizer.Agents.initializer import Initializer

sm_ontology = "db/Ontology/assistant.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()


def main():

    print('Por favor, diga a língua para o sistema ("pt" ou "en")')
    print('> ')
    language = input()
    dict_output = {'mode': 'regular'}
    json_output = json.loads(json.dumps(dict_output))  # Clausula semântica (json) do OutputGenerator para o Semantizador
    file = open("tests/tests_phrases/frases_teste.txt", mode="r")
    dm = DialogManager()
    print("REMOVER PARA DEPLOY !!!!!!!!!!")
    dm.og.set_language(language)
    dm.start()
    semanticizer = Semanticizer('response', language, initial_vars, user_id=1)
    #for line in file:  # testes em frases pre-escritas
    i = 0
    while True:
            print("Digite a frase")
            line = input()
            id_name = int(input("Digite o ID"))
            semanticizer.intent_entities = {}
            my_json = semanticizer.semantize(line)
            print("JSON: ")
            print(my_json)
            message = DialogMessage.from_json((my_json))
            # altera entre as duas pessoas para simular corretamente
            message.id_user = id_name
            # if i == 1:
            #     i = 0
            #     message.id_user = 3
            # else:
            #     i = 1
            #     message.id_user = 1

            print("with_list%s\nintent%s\ndate%s\nhour%s\nplace%s" % (message.with_list, message.intent, message.date, message.hour, message.place))
            dm.dispatch_msg(message)


if __name__ == '__main__':
    main()
