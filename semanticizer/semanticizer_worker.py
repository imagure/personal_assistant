from semanticizer.Semanticizer import Semanticizer
from semanticizer.Agents.synsets_NLTK import NLTKSynsets
from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
import queue
import threading
import psycopg2

dm = DialogManager()
dm.start()
synsets = NLTKSynsets()

with open("configs/databases.json") as f:
    data = json.load(f)


class SemanticizerWorker(threading.Thread):

    def __init__(self, language):
        self.language = language
        if language == 'pt':
            self.semanticizer = Semanticizer('response', 'pt', synsets)
        elif language == 'en':
            self.semanticizer = Semanticizer('response', 'en', synsets)
        self.input_queue = queue.Queue()
        self.id = None
        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
        threading.Thread.__init__(self)

    def dispatch_msg(self, msg):
        self.input_queue.put(msg)

    def dispatch_channel(self, channel_id):
        query = """SELECT ID FROM USUARIO WHERE FORMACONTATO = (%s)"""
        cursor = self.con.cursor()
        cursor.execute(query, (channel_id, ))
        ids =  cursor.fetchall()
        if len(ids) == 1:
            self.id = ids[0][0]

    def run(self):
        while True:
            if not self.input_queue.empty():
                if self.id is not None:
                    msg = self.input_queue.get()
                    my_json = self.semanticizer.semantize(msg)
                    message = DialogMessage.from_json(my_json)
                    message.id_user = self.id
                    dm.dispatch_msg(message)
                    if self.language == 'pt':
                        dm.og.set_language('pt')
                    elif self.language == 'en':
                        dm.og.set_language('en')
