import queue
import threading
import random

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
        slack_users = []
        contacts_ids = []
        user_id = None

        self.send_message(user_name, channel_id, answer="wait")

        insert_success = db_interface.insert(user_name, user_slack_id, channel_id)
        if insert_success:
            user_id = db_interface.search_user(channel_id)
            insert_new_user(initial_vars.graph, user_name, user_id)
            slack_users = self.slack.users_list(user_slack_id)

        if slack_users and insert_success:
            contacts_ids = db_interface.search_users(slack_users)

        if contacts_ids and slack_users and insert_success and user_id is not None:
            insert_contacts(initial_vars.graph, user_id, contacts_ids)
            self.send_message(user_name, channel_id, answer="success")
        else:
            if not insert_success:
                self.send_message(user_name, channel_id, answer="insert_fail")
            elif not slack_users:
                self.send_message(user_name, channel_id, answer="contacts_slack_fail")
            elif not contacts_ids:
                self.send_message(user_name, channel_id, answer="contacts_db_fail")

    def send_message(self, user_name, channel_id, answer):

        response = ""

        if answer == "wait":
            if self.language == 'pt':
                response = random.choice(out_data_pt["Outputs"]["new_user_wait"]).format(user_name)
            elif self.language == 'en':
                response = random.choice(out_data_en["Outputs"]["new_user_wait"]).format(user_name)
        elif answer == "success":
            if self.language == 'pt':
                response = random.choice(out_data_pt["Outputs"]["new_user_success"]).format(user_name)
            elif self.language == 'en':
                response = random.choice(out_data_en["Outputs"]["new_user_success"]).format(user_name)
        elif answer == "insert_fail":
            if self.language == 'pt':
                response = random.choice(out_data_pt["Outputs"]["new_user_insert_fail"]).format(user_name)
            elif self.language == 'en':
                response = random.choice(out_data_en["Outputs"]["new_user_insert_fail"]).format(user_name)
        elif answer == "contacts_slack_fail":
            if self.language == 'pt':
                response = random.choice(out_data_pt["Outputs"]["new_user_contacts_slack_fail"]).format(user_name)
            elif self.language == 'en':
                response = random.choice(out_data_en["Outputs"]["new_user_contacts_slack_fail"]).format(user_name)
        elif answer == "contacts_db_fail":
            if self.language == 'pt':
                response = random.choice(out_data_pt["Outputs"]["new_user_contacts_db_fail"]).format(user_name)
            elif self.language == 'en':
                response = random.choice(out_data_en["Outputs"]["new_user_contacts_db_fail"]).format(user_name)

        response_dict = {"text": response, "user_id": channel_id, "existance": 'false'}
        message_sender.dispatch_msg(response_dict)

        print("-" * 20)
        print(response)
        print("-" * 20)
