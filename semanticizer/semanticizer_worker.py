import queue
import threading

import psycopg2

from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
from semanticizer.Agents.initializer import Initializer
from semanticizer.Semanticizer import Semanticizer
from output_generator import message_sender as msender
from client_interface.slack_client import SlackHelper

message_sender = msender.MessageSender()
message_sender.start()

dm = DialogManager()
dm.start()
sm_ontology = "db/Ontology/assistant.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()

with open("configs/databases.json") as f:
    data = json.load(f)


class SemanticizerWorker(threading.Thread):

    def __init__(self, language):
        self.language = language
        self.input_queue = queue.Queue()
        self.id = None
        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
        self.slack = SlackHelper()
        threading.Thread.__init__(self)

    def dispatch_msg(self, msg, channel_id, user_name, user_slack_id):
        query = """SELECT ID FROM USUARIO WHERE FORMACONTATO = (%s)"""
        cursor = self.con.cursor()
        cursor.execute(query, (channel_id, ))
        # Substituir por:
        # cursor.execute(query, (user_slack_id, ))
        ids = cursor.fetchall()
        if len(ids) == 1:
            user_id = ids[0][0]
            self.input_queue.put([msg, user_id])
        else:
            # adicionar user ao DB:
            # db_interface.add(user_name, user_id, channel_id)
            # fazer busca por contatos aqui
            # slack_users = self.slack.users_list(user_id)
            # adicionar slack_users à ontologia
            # ontology_interface.add(slack_users)
            response = ""
            if self.language == 'pt':
                response = "{}, não conheço seus contatos!" \
                           " Não consigo marcar seu compromisso".format(user_name)
            elif self.language == 'en':
                response = "{}, I don't know your contacts! " \
                           "I can't schedule your meeting".format(user_name)
            print("-" * 20)
            print(response)
            print("-" * 20)
            response_dict = {"text": response, "user_id": channel_id, "existance": 'false'}
            message_sender.dispatch_msg(response_dict)

    def run(self):
        while True:
            if not self.input_queue.empty():
                msg = self.input_queue.get()
                phrase = msg[0]
                user_id = msg[1]

                if self.language == 'pt':
                    semanticizer = Semanticizer('response', 'pt', initial_vars, user_id)
                    dm.og.set_language('pt')
                else:
                    semanticizer = Semanticizer('response', 'en', initial_vars, user_id)
                    dm.og.set_language('en')

                my_json = semanticizer.semantize(phrase)
                message = DialogMessage.from_json(my_json)
                message.id_user = user_id
                dm.dispatch_msg(message)
