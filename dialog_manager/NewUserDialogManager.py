import queue
import threading

from client_interface.slack_client import SlackHelper
from db.Ontology.ontology_interface import *
from db.sql.db_interface import DbInterface
from dialog_message.new_user_message import *
from output_generator.OutputGenerator import OutputGenerator

db_interface = DbInterface()

og = OutputGenerator()
og.start()


class NewUserDialogManager(threading.Thread):

    def __init__(self, initial_vars):

        self.language = None
        self.input_queue = queue.Queue()
        self.slack = SlackHelper()
        self.initial_vars = initial_vars
        self.pending_requests_ids = {}
        threading.Thread.__init__(self)

    def set_language(self, language):

        self.language = language

    def dispatch_msg(self, msg):

        self.input_queue.put(msg)

    def run(self):

        while True:
            if not self.input_queue.empty():
                msg = self.input_queue.get()
                if self.first_contact(msg):
                    self._new_user_request_first_name(msg)
                elif self.second_contact(msg):
                    if msg["valid_name"]:
                        self._new_user_request_last_name(msg)
                    else:
                        self._new_user_request_valid_name(msg)
                else:
                    self._add_user_last_name(msg)
                    self._add_new_user(msg)

    def first_contact(self, msg):

        # user_slack_id = msg["user_slack_id"] trocar por isso aqui depois
        user_slack_id = msg["channel_id"]
        if user_slack_id not in self.pending_requests_ids:
            return True
        return False

    def second_contact(self, msg):

        # user_slack_id = msg["user_slack_id"] trocar por isso aqui depois
        user_slack_id = msg["channel_id"]
        if user_slack_id in self.pending_requests_ids \
                and self.pending_requests_ids[user_slack_id]["first_name"] is None \
                and self.pending_requests_ids[user_slack_id]["last_name"] is None:
            return True
        return False

    def _new_user_request_first_name(self, msg):

        user_name = msg["user_name"]
        user_slack_id = msg["user_slack_id"]
        channel_id = msg["channel_id"]

        self._send_output(user_name, channel_id, answer="new_user_request_first_name")

        # self.pending_requests_ids[user_slack_id] = {"first_name": None, "last_name": None} mudar para isso depois
        self.pending_requests_ids[channel_id] = {"first_name": None, "last_name": None}

    def _new_user_request_valid_name(self, msg):
        invalid_name = msg["user_requested_name"]
        user_slack_id = msg["user_slack_id"]
        channel_id = msg["channel_id"]

        self._send_output(invalid_name, channel_id, answer="new_user_request_valid_name")

    def _new_user_request_last_name(self, msg):

        first_name = msg["user_requested_name"]
        user_slack_id = msg["user_slack_id"]
        channel_id = msg["channel_id"]

        self._send_output(first_name, channel_id, answer="new_user_request_last_name")

        # self.pending_requests_ids[user_slack_id]["first_name"] = first_name mudar para isso depois
        self.pending_requests_ids[channel_id]["first_name"] = first_name

    def _add_user_last_name(self, msg):

        # user_slack_id = msg["user_slack_id"] mudar para isso depois
        user_slack_id = msg["channel_id"]
        last_name = msg["user_requested_name"]
        self.pending_requests_ids[user_slack_id]["last_name"] = last_name

    def _add_new_user(self, msg):

        # user_slack_id = msg["user_slack_id"] mudar para isso depois
        user_slack_id = msg["channel_id"]

        channel_id = msg["channel_id"]
        user_name = self.pending_requests_ids[user_slack_id]["first_name"] + " " + \
                    self.pending_requests_ids[user_slack_id]["last_name"]
        slack_users = []
        contacts_ids = []
        user_id = None

        self._send_output(user_name, channel_id, answer="new_user_wait")

        correct_channel_id = self.slack.find_user_channel(msg["user_slack_id"])

        insert_success = db_interface.insert(user_name, user_slack_id, correct_channel_id)

        if insert_success:
            user_id = db_interface.search_user(correct_channel_id)
            insert_new_user(self.initial_vars.graph, self.pending_requests_ids[user_slack_id], user_id)
            slack_users = self.slack.users_list(msg["user_slack_id"])

        if slack_users and insert_success:
            contacts_ids = db_interface.search_users(slack_users)

        if contacts_ids and slack_users and insert_success and user_id is not None:
            insert_contacts(self.initial_vars.graph, user_id, contacts_ids)
            self._send_output(user_name, channel_id, answer="new_user_success")
            # del self.pending_requests_ids[user_slack_id] # mudar para user_slack_id
            del self.pending_requests_ids[channel_id] # mudar para user_slack_id
        else:
            if not insert_success:
                self._send_output(user_name, channel_id, answer="new_user_insert_fail")
            elif not slack_users:
                self._send_output(user_name, channel_id, answer="new_user_contacts_slack_fail")
            elif not contacts_ids:
                self._send_output(user_name, channel_id, answer="new_user_contacts_db_fail")

    def _send_output(self, user_name, channel_id, answer):

        response_dict = {"intent": answer,
                         "id_user": channel_id,
                         "person_known": user_name,
                         }

        response_json = json.dumps(response_dict, indent=4, ensure_ascii=False)
        message = NewUserDialogMessage.from_json(response_json)
        og.set_language(self.language)
        og.dispatch_new_user_msg(message)
