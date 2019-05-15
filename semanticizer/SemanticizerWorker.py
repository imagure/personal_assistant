import queue
import threading

from client_interface.slack_client import SlackHelper
from db.sql.db_interface import DbInterface
from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
from output_generator import NewUserInterfaceOutputGenerator as nu_og
from semanticizer.Agents.initializer import Initializer
from semanticizer.Semanticizer import Semanticizer

db_interface = DbInterface()

dm = DialogManager()
dm.start()

sm_ontology = "db/Ontology/assistant2.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()

new_user_og = nu_og.NewUserInterfaceOutputGenerator(initial_vars)
new_user_og.start()


class SemanticizerWorker(threading.Thread):

    def __init__(self):

        self.language = None
        self.input_queue = queue.Queue()
        self.slack = SlackHelper()
        threading.Thread.__init__(self)

    def set_language(self, language):

        self.language = language

    def dispatch_msg(self, msg, channel_id, user_name, user_slack_id):

        user_id = db_interface.search_user(channel_id)  # mudar para 'user_slack_id'
        if user_id:
            msg = {"new_user": "no", "msg": msg, "user_id": user_id}
        else:
            msg = {"new_user": "yes", "channel_id": channel_id, "user_name": user_name, "user_slack_id": user_slack_id}
        self.input_queue.put(msg)

    def run(self):

        while True:
            if not self.input_queue.empty():
                msg = self.input_queue.get()
                if msg["new_user"] == "no":
                    self._semantic_routine(msg)
                elif msg["new_user"] == "yes":
                    new_user_og.set_language(self.language)
                    new_user_og.dispatch_msg(msg)

    def _semantic_routine(self, msg):

        phrase = msg["msg"]
        user_id = msg["user_id"]

        semanticizer = Semanticizer('response', initial_vars, user_id)
        semanticizer.set_language(self.language)
        dm.og.set_language(self.language)

        my_json = semanticizer.validate_and_semantize(phrase)
        message = DialogMessage.from_json(my_json)
        message.id_user = user_id
        dm.dispatch_msg(message)
