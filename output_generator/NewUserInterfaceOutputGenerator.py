import queue
import threading
import random

from output_generator import message_sender as msender
from client_interface.slack_client import SlackHelper
from db.sql.db_interface import DbInterface
from db.Ontology.ontology_interface import *

db_interface = DbInterface()

message_sender = msender.MessageSender()
message_sender.start()


class NewUserInterfaceOutputGenerator(threading.Thread):

    def __init__(self, initial_vars):

        self.language = None
        self.data = None
        self.input_queue = queue.Queue()
        self.slack = SlackHelper()
        self.initial_vars = initial_vars
        threading.Thread.__init__(self)

    def set_language(self, language):

        self.language = language
        if self.language == "pt":
            f = open("configs/output_phrases_pt.json")
            self.data = json.load(f)
        elif self.language == "en":
            f = open("configs/output_phrases_en.json")
            self.data = json.load(f)

    def dispatch_msg(self, msg):

        self.input_queue.put(msg)

    def run(self):

        while True:
            if not self.input_queue.empty():
                self._new_user_routine(self.input_queue.get())

    def _new_user_routine(self, msg):

        user_name = msg["user_name"]
        user_slack_id = msg["user_slack_id"]
        channel_id = msg["channel_id"]
        slack_users = []
        contacts_ids = []
        user_id = None

        self._send_output(user_name, channel_id, answer="wait")

        insert_success = db_interface.insert(user_name, user_slack_id, channel_id)
        if insert_success:
            user_id = db_interface.search_user(channel_id)
            insert_new_user(self.initial_vars.graph, user_name, user_id)
            slack_users = self.slack.users_list(user_slack_id)
        if slack_users and insert_success:
            contacts_ids = db_interface.search_users(slack_users)

        if contacts_ids and slack_users and insert_success and user_id is not None:
            insert_contacts(self.initial_vars.graph, user_id, contacts_ids)
            self._send_output(user_name, channel_id, answer="success")
        else:
            if not insert_success:
                self._send_output(user_name, channel_id, answer="insert_fail")
            elif not slack_users:
                self._send_output(user_name, channel_id, answer="contacts_slack_fail")
            elif not contacts_ids:
                self._send_output(user_name, channel_id, answer="contacts_db_fail")

    def _send_output(self, user_name, channel_id, answer):

        response = self._formulate_response(answer, user_name)

        response_dict = {"text": response, "user_id": channel_id, "existance": 'false'}
        message_sender.dispatch_msg(response_dict)

        print("-" * 20)
        print(response)
        print("-" * 20)

    def _formulate_response(self, answer, user_name):

        response = ""
        if answer == "wait":
            response = random.choice(self.data["Outputs"]["new_user_wait"]).format(user_name)
        elif answer == "success":
            response = random.choice(self.data["Outputs"]["new_user_success"]).format(user_name)
        elif answer == "insert_fail":
            response = random.choice(self.data["Outputs"]["new_user_insert_fail"]).format(user_name)
        elif answer == "contacts_slack_fail":
            response = random.choice(self.data["Outputs"]["new_user_contacts_slack_fail"]).format(user_name)
        elif answer == "contacts_db_fail":
            response = random.choice(self.data["Outputs"]["new_user_contacts_db_fail"]).format(user_name)

        return response
