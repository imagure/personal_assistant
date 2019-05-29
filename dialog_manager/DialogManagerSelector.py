import queue
import threading
from db.sql.db_interface import DbInterface
from dialog_manager.dialog_manager import DialogManager
import dialog_manager.dialog_manager_states
from queue import Queue
db_interface = DbInterface()
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
                    keysEncontradas = []
                    for key in self.users_active_meeting.keys():
                        if self.users_active_meeting[key] == id_meeting:
                            keysEncontradas.append(key)
                    for key in keysEncontradas:
                        del self.users_active_meeting[key]


    '''
        Given the input message, select the aproprieated dm for the work
    '''

    def _dm_select(self, message):
        # caso esteja no get initial info, retorna independente de qualquer coisa
        if message.id_user in self.users_active_meeting.keys():
            dm = self.dm_dict[self.users_active_meeting[message.id_user]]
            if dm.state.__name__ == 'InitialInfo':
                self.dm = self.dm_dict[self.users_active_meeting[message.id_user]]
                return
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

    def _recover_old_dm(self, id_meeting):

        if id_meeting in self.dm_dict.keys():
            self.dm = self.dm_dict[id_meeting]
        else:
            # só recupera da memória encontro que já foi marcado
            infos = db_interface.search_all_meeting_info(id_meeting)
            print(infos)
            self.dm = DialogManager(infos[0][0], self, id_meeting)
            self.dm.state = dialog_manager.dialog_manager_states.InfoCompleted(self.dm)
            self.dm.with_list = []
            self.dm.where = infos[0][1]
            self.dm.date = infos[0][4]
            self.dm.commitment = infos[0][3]
            self.dm.hour = infos[0][2]

            participantes = db_interface.search_clients_from_meeting(id_meeting)
            for pessoa in participantes:
                self.dm.with_list.append(pessoa[0])


            db_interface.update_meeting(id_meeting, infos)

            # self.dm.dispatch_msg('load_queues')
            self.dm.start()
            # Coloquei essa mensagem para aviso de que reunião voltou a discussão
            self.dm.notify_all_members_selector('notify_revival')
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

        print("\n========= find_meeting.start ==========")

        hit_meetings = []

        print("enquanto a lista de pessoas não funcionará")

        if message.person_know:
            print("\n==> Procurando todas os compromissos:")
            found = self._search_through_all_meetings(message, hit_meetings)
            if found:
                return

        if message.place_unknown:
            print("\n==> Procurando por 'onde (unknown)':")
            found = self._search_by_specific_info(message.place_unknown, hit_meetings, 'onde',
                                                  message.place_unknown[0], message.id_user)
            if found:
                return

        if message.place_known:
            print("\n==> Procurando por 'onde (known)':")
            found = self._search_by_specific_info(message.place_known, hit_meetings, 'onde',
                                                  message.place_known[0], message.id_user)
            if found:
                return

        if message.date:
            print("\n==> Procurando por 'dia':")
            found = self._search_by_specific_info(message.date, hit_meetings, 'dia',
                                                  message.date[0], message.id_user)
            if found:
                return

        if message.hour:
            print("\n==> Procurando por 'hora':")
            found = self._search_by_specific_info(message.hour, hit_meetings, 'quando',
                                                  message.hour[0], message.id_user)
            if found:
                return

        if len(hit_meetings) == 0:
            print("TODO: nenhum encontro foi encontrado")
        else:
            print("TODO: mensagem para desambiguar encontros")

        print("\n========= find_meeting.end ==========")
        self.dm = None

    def _search_through_all_meetings(self, message, hit_meetings):

        if message.person_know is not None and message.person_know != []:
            candidate_meetings = db_interface.search_meetings_from_client(message.id_user)
            for meeting in candidate_meetings:
                candidate_users = db_interface.search_clients_from_meeting(meeting[0])
                candidatos = []
                hit = True
                for user in candidate_users:
                    candidatos.append(user[0])
                for person in message.person_know:
                    if person not in candidatos:
                        hit = False
                if hit:
                    hit_meetings.append(meeting[0])
            # here hit_meetings = [] contains all meetings id that have the data input from user
            if len(hit_meetings) == 1:
                # encontramos o encontro desejado
                # self._save_old_dm()
                self._recover_old_dm(hit_meetings[0])
                return True
            return False

    def _search_by_specific_info(self, message, hit_meetings, column, info, user_id):

        if message is not None and message != []:
            if hit_meetings != []:
                for id_meeting in hit_meetings:
                    result = db_interface.search_info_from_meeting(column, id_meeting)
                    if result[0][0][0] not in message:
                        hit_meetings.remove(id_meeting)
            else:
                results = db_interface.search_meeting_joining_tables(column, info, user_id)
                for result in results:
                    hit_meetings.append(result[0])
            if len(hit_meetings) == 1:
                self._recover_old_dm(hit_meetings[0])
                return True
            return False
