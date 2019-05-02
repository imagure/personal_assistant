import queue
import threading

from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
from semanticizer.Agents.initializer import Initializer
from semanticizer.Semanticizer import Semanticizer
from output_generator import message_sender as msender
from client_interface.slack_client import SlackHelper
from db.db_interface import db_interface
from db.Ontology.ontology_interface import *

db_interface = db_interface()

message_sender = msender.MessageSender()
message_sender.start()

dm = DialogManager()
dm.start()

sm_ontology = "db/Ontology/assistant2.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()

with open("configs/output_phrases_pt.json") as g:
    out_data_pt = json.load(g)
with open("configs/output_phrases_en.json") as h:
    out_data_en = json.load(h)


class SemanticizerWorker(threading.Thread):

    def __init__(self, language):
        self.language = language
        self.input_queue = queue.Queue()
        self.id = None
        self.slack = SlackHelper()
        threading.Thread.__init__(self)

    def dispatch_msg(self, msg, channel_id, user_name, user_slack_id):
        user_id = db_interface.search_user(channel_id)  # mudar para 'user_slack_id'
        if user_id:
            msg = {"new_user": "no", "msg": msg, "user_id": user_id}
            self.input_queue.put(msg)
        else:
            msg = {"new_user": "yes", "channel_id": channel_id, "user_name": user_name, "user_slack_id": user_slack_id}
            self.input_queue.put(msg)

    def run(self):
        while True:
            if not self.input_queue.empty():
                msg = self.input_queue.get()
                if msg["new_user"] == "no":
                    self.semantic_routine(msg)
                elif msg["new_user"] == "yes":
                    self.new_user_routine(msg)

    def semantic_routine(self, msg):
        phrase = msg["msg"]
        user_id = msg["user_id"]

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

    def new_user_routine(self, msg):
        user_name = msg["user_name"]
        user_slack_id = msg["user_slack_id"]
        channel_id = msg["channel_id"]

        db_interface.insert(user_name, user_slack_id, channel_id)

        slack_users = self.slack.users_list(user_slack_id)

        user_id = db_interface.search_user(channel_id)
        contacts_ids = db_interface.search_users(slack_users)

        insert_new_user(initial_vars.graph, user_name, user_id)
        if contacts_ids:
            insert_contacts(initial_vars.graph, user_id, contacts_ids)

        self.send_wait_message(user_name, channel_id)

    def send_wait_message(self, user_name, channel_id):
        response = ""
        if self.language == 'pt':
            response = out_data_pt["Outputs"]["new_user_response"][0].format(user_name)
        elif self.language == 'en':
            response = out_data_en["Outputs"]["new_user_response"][0].format(user_name)
        print("-" * 20)
        print(response)
        print("-" * 20)
        response_dict = {"text": response, "user_id": channel_id, "existance": 'false'}
        message_sender.dispatch_msg(response_dict)
