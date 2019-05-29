import queue
import threading

from db.sql.db_interface import DbInterface
from dialog_manager.DialogManagerSelector import DialogManagerSelector
from dialog_message.dialog_message import *
from dialog_manager import NewUserDialogManager as nui
from semanticizer.Agents.initializer import Initializer
from semanticizer.Semanticizer import Semanticizer

db_interface = DbInterface()

sm_ontology = "db/Ontology/assistant2.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()

new_user_og = nui.NewUserDialogManager(initial_vars)
new_user_og.start()

dm_selector = DialogManagerSelector()
dm_selector.start()


class SemanticizerWorker(threading.Thread):

    def __init__(self):

        self.language = None
        self.input_queue = queue.Queue()
        self.new_user_queue = queue.Queue()
        threading.Thread.__init__(self)

    def set_language(self, language):

        self.language = language

    def dispatch_msg(self, msg, channel_id, user_name, user_slack_id):

        user_id = db_interface.search_user(channel_id)  # mudar para 'user_slack_id'
        if user_id:
            msg = {"msg": msg,
                   "user_id": user_id}
            self.input_queue.put(msg)
        else:
            msg = {"channel_id": channel_id,
                   "user_name": user_name,
                   "user_requested_name": msg,
                   "valid_name": True,
                   "user_slack_id": user_slack_id}
            self.new_user_queue.put(msg)

    def run(self):

        while True:

            if not self.input_queue.empty():
                msg = self.input_queue.get()
                self._semantic_routine(msg)

            elif not self.new_user_queue.empty():
                msg = self.new_user_queue.get()
                if new_user_og.first_contact(msg):
                    self._new_user_request(msg)
                elif new_user_og.second_contact(msg):
                    self._new_user_validate_name(msg)
                else:
                    self._new_user_request(msg)

    def _semantic_routine(self, msg):

        phrase = msg["msg"]
        user_id = msg["user_id"]

        semanticizer = Semanticizer('response', initial_vars, user_id=user_id)
        semanticizer.set_language(self.language)

        my_json = semanticizer.validate_and_semantize(phrase)
        message = DialogMessage.from_json(my_json)
        message.id_user = user_id
        dm_selector.dispatch_msg(message, self.language)

    def _new_user_request(self, msg):

        new_user_og.set_language(self.language)
        new_user_og.dispatch_msg(msg)

    def _new_user_validate_name(self, msg):
        semanticizer = Semanticizer('response', initial_vars)
        name = semanticizer.find_name_only(msg["user_requested_name"], self.language)
        if not name:
            msg["valid_name"] = False
        new_user_og.set_language(self.language)
        new_user_og.dispatch_msg(msg)
