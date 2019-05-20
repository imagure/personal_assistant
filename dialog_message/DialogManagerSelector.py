import pickle as pk
import queue
import threading

from db.sql.db_interface import DbInterface
from dialog_manager.dialog_manager import DialogManager
import dialog_manager.dialog_manager_states
db_interface = DbInterface()
from queue import Queue
# for each id_user, contains id_meeting of the last user interaction
# users_active_meeting = {}


class DialogManagerSelector(threading.Thread):

    def __init__(self):

        self.input_queue = queue.Queue()
        threading.Thread.__init__(self)
        self.dm = None
        self.users_active_meeting = {}
        self.dm_dict = {}
        self.dm_to_kill = Queue()

    def dispatch_msg(self, message, language):
        input_info = {"message": message, "language": language}
        self.input_queue.put(input_info)

    def kill_dm(self, id_meeting):
        self.dm_to_kill.put(id_meeting)


    def run(self):

        while True:
            if not self.input_queue.empty():
                input_info = self.input_queue.get()
                message = input_info["message"]
                language = input_info["language"]

                self._dm_select(message)
                if self.dm is not None:
                    self.dm.og.set_language(language)
                    self.dm.dispatch_msg(message)
                    self.users_active_meeting[message.id_user] = self.dm.id_meeting
            if not self.dm_to_kill.empty():
                id_meeting = self.dm_to_kill.get()
                if id_meeting in self.dm_dict.keys():
                    del self.dm_dict[id_meeting]


    '''
        Given the input message, select the aproprieated dm for the work
    '''

    def _dm_select(self, message):
        if 'marcar_compromisso' in message.intent:
            self._select_new_meeting(message.id_user)
        elif message.id_user in self.users_active_meeting.keys():
            self._select_active_meeting(message.id_user)
        else:
            self._find_meeting(message)

    def _save_old_dm(self):
        print('do nothing?')
        if self.dm is None:
            return
        # self.dm.dispatch_msg('save_queues')
        # if self.dm is not None:
        #     with open(str(self.dm.id_meeting), 'wb') as dm_file:
        #        pk.dump(self.dm, dm_file)

    def _recover_old_dm(self, id_meeting):
        if id_meeting in self.dm_dict.keys():
            self.dm = self.dm_dict[id_meeting]
        else:
            select_query = """SELECT IDMEETINGOWNER, ONDE, QUANDO, OQUE, DIA FROM ENCONTRO WHERE ID = (%s)"""
            cursor = db_interface.con.cursor()
            cursor.execute(select_query, (id_meeting,))
            temp = cursor.fetchall()
            print(temp)
            self.dm = DialogManager(temp[0][0], self, id_meeting)
            self.dm.with_list = []
            self.dm.where = temp[0][1]
            self.dm.date = temp[0][4]
            self.dm.commitment = temp[0][3]
            self.dm.hour = temp[0][2]
            select_query = """SELECT IDCLIENTE FROM LISTAENCONTRO WHERE IDENCONTRO = (%s)"""
            cursor.execute(select_query, (id_meeting,))
            participantes = cursor.fetchall()
            for pessoa in participantes:
                self.dm.with_list.append(pessoa[0])
            self.dm.state = dialog_manager.dialog_manager_states.InfoCompleted(self.dm)
            update_query = """UPDATE LISTAENCONTRO SET ACEITOU = %s WHERE IDENCONTRO = %s and IDCLIENTE <> %s"""
            cursor.execute(update_query, (0, id_meeting, temp[0][0]))
            # self.dm.dispatch_msg('load_queues')
            self.dm.start()
            self.dm_dict[id_meeting] = self.dm

    def _select_new_meeting(self, id_user):
        # self._save_old_dm()
        self.dm = DialogManager(id_user, self)
        self.dm_dict[self.dm.id_meeting] = self.dm
        self.dm.start()

    def _select_active_meeting(self, id_user):
        # self._save_old_dm()
        self._recover_old_dm(self.users_active_meeting[id_user])
        # self.dm = self.dm_dict[self.users_active_meeting[id_user]]

    def _find_meeting(self, message):
        cursor = db_interface.con.cursor()
        hit_meetings = []
        print("enquanto a lista de pessoas não funcionará")
        if message.person_know is not None and message.person_know != []:
            select_query = """SELECT distinct(IDENCONTRO) 
                                  FROM ListaEncontro 
                                  WHERE idcliente = (%s)"""
            cursor.execute(select_query, (message.id_user,))
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
                # self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.place_known is not None and message.place_known != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT onde from encontro where id = (%s)
                                       """
                    cursor.execute(select_query, (idmeeting,))
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
                # self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.date is not None and message.date != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT dia from encontro where id = (%s)
                                       """
                    cursor.execute(select_query, (idmeeting,))
                    result = cursor.fetchall()
                    if result[0] not in message.date:
                        hit_meetings.remove(idmeeting)
            else:
                select_query = """SELECT encontro.ID from encontro  
                    inner join listaencontro on encontro.id = listaencontro.idencontro 
                    where encontro.dia = (%s) and listaencontro.idcliente = (%s)
                    """
                cursor.execute(select_query, (message.date[0], message.id_user))
                results = cursor.fetchall()
                for result in results:
                    hit_meetings.append(result[0])
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                # self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if message.hour is not None and message.hour != []:
            # querys precisam procurar apenas nos ids já colocados como candidatos
            if hit_meetings != []:
                for idmeeting in hit_meetings:
                    select_query = """SELECT quando from encontro where id = (%s)
                                       """
                    cursor.execute(select_query, (idmeeting,))
                    result = cursor.fetchall()
                    if result[0] not in message.hour:
                        hit_meetings.remove(idmeeting)
            else:
                select_query = """SELECT encontro.ID from encontro  
                    inner join listaencontro on encontro.id = listaencontro.idencontro 
                    where encontro.quando = (%s) and listaencontro.idcliente = (%s)
                    """
                cursor.execute(select_query, (message.hour[0], message.id_user))
                results = cursor.fetchall()
                for result in results:
                    hit_meetings.append(result[0])
            if (len(hit_meetings) == 1):
                # encontramos o encontro desejado
                # self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return
        if len(hit_meetings) == 0:
            print("TODO: nenhum encontro foi encontrado")
        else:
            print("TODO: mensagem para desambiguar encontros")
