import queue
import threading
import pickle as pk

from client_interface.slack_client import SlackHelper
from db.sql.db_interface import DbInterface
from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
from output_generator import NewUserInterfaceOutputGenerator as nu_og
from semanticizer.Agents.initializer import Initializer
from semanticizer.Semanticizer import Semanticizer


db_interface = DbInterface()
# for each id_user, contains id_meeting of the last user interaction
users_active_meeting = {}

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
        self.dm = None
        # self.dm.start()

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
        if self.dm is not None:
            self.dm.og.set_language(self.language)

        my_json = semanticizer.semantize(phrase)
        message = DialogMessage.from_json(my_json)
        message.id_user = user_id
        self._dm_select()
        if self.dm is not None:
            self.dm.dispatch_msg(message)
            users_active_meeting[message.id_user] = self.dm.id_meeting

    '''
        Given the input message, select the aproprieated dm for the work
    '''
    def _dm_select(self, message):
        if 'marcar_compromisso' in message.intent:
            self._select_new_meeting(message.id_user)
        elif message.id_user in users_active_meeting.keys():
            self._select_active_meeting(message.id_user)
        else:
            self._find_meeting(message)

    def _save_old_dm(self):
        if self.dm is not None:
            with open(str(self.dm.id_meeting), 'wb') as dm_file:
                pk.dump(self.dm, dm_file)

    def _recover_old_dm(self, id_meeting):
        with open(str(id_meeting), 'rb') as dm_file:
            self.dm = pk.load(dm_file)

    def _select_new_meeting(self, id_user):
        self._save_old_dm()
        self.dm = DialogManager(id_user)
        self.dm.start()

    def _select_active_meeting(self, id_user):
        self._save_old_dm()
        self._recover_old_dm(users_active_meeting[id_user])

    def _find_meeting(self, message):
        cursor = DbInterface.con.cursor()
        hit_meetings = []
        print("enquanto a lista de pessoas não funcionará")
        if message.person_know is not None and message.person_know != []:
            select_query = """SELECT distinct(IDENCONTRO) 
                              FROM ListaEncontro 
                              WHERE idcliente = (%s)"""
            cursor.execute(select_query, (message.id_user, ))
            candidate_meetings = cursor.fetchall()
            hit_meetings = []
            for meeting in candidate_meetings:
                select_query = """SELECT distinct(idcliente) 
                                              FROM ListaEncontro 
                                              WHERE idencontro = (%s)"""
                cursor.execute(select_query, (meeting[0],))
                candidate_users = cursor.fetchall()
                hit = True
                for user in candidate_users:
                    if user[0] not in message.person_know:
                        hit = False
                if hit:
                    hit_meetings.append(meeting[0])
            # here hit_meetings = [] contains all meetings id that have the data input from user
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.place_known is not None and message.place_known != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT onde from encontro where id = (%s)
                                   """
                    cursor.execute(select_query, (idmeeting, ))
                    result = cursor.fetchall()
                    if result[0] not in message.place_known:
                        hit_meetings.remove(idmeeting)
            else:
                select_query = """SELECT encontro.ID from encontro  
                inner join listaencontro on encontro.id = listaencontro.idencontro 
                where encontro.onde = (%s) and listaencontro.idcliente = (%s)
                """
                cursor.execute(select_query, (message.place_known, message.id_user))
                results = cursor.fetchall()
                for result in results:
                    hit_meetings.append(result[0])
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.date is not None and message.date != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT dia from encontro where id = (%s)
                                   """
                    cursor.execute(select_query, (idmeeting, ))
                    result = cursor.fetchall()
                    if result[0] not in message.date:
                        hit_meetings.remove(idmeeting)
            else:
                select_query = """SELECT encontro.ID from encontro  
                inner join listaencontro on encontro.id = listaencontro.idencontro 
                where encontro.dia = (%s) and listaencontro.idcliente = (%s)
                """
                cursor.execute(select_query, (message.date, message.id_user))
                results = cursor.fetchall()
                for result in results:
                    hit_meetings.append(result[0])
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.hour is not None and message.hour != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT quando from encontro where id = (%s)
                                   """
                    cursor.execute(select_query, (idmeeting, ))
                    result = cursor.fetchall()
                    if result[0] not in message.hour:
                        hit_meetings.remove(idmeeting)
            else:
                select_query = """SELECT encontro.ID from encontro  
                inner join listaencontro on encontro.id = listaencontro.idencontro 
                where encontro.quando = (%s) and listaencontro.idcliente = (%s)
                """
                cursor.execute(select_query, (message.hour, message.id_user))
                results = cursor.fetchall()
                for result in results:
                    hit_meetings.append(result[0])
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if len(hit_meetings) == 0:
            print("TODO: nenhum encontro foi encontrado")
        else:
            print("TODO: mensagem para desambiguar encontros")
















