from dialog_manager.dialog_manager_states import *
from dialog_message.dialog_message import *
import output_generator.OutputGenerator as og
from queue import Queue
# from persistqueue import Queue
import threading
import time
import json
import psycopg2
import pickle as pk
from db.sql.db_interface import *

ask_list = {'ask_what', 'ask_when', 'ask_with', 'ask_withlist', 'ask_where'}

with open("configs/databases.json") as f:
    data = json.load(f)


class DialogManager(threading.Thread):
    def __init__(self, id_meeting_owner, dms, id_meeting=None):
        """ Initialize the components. """

        # Start with a default state.
        self.state = Idle("", self)
        # data to be get from user
        # basic info attributes
        self.with_list = []
        self.where = []
        self.when = []
        self.date = []
        self.hour = []
        self.commitment = []
        self.income_data = []
        #self.id_meeting = -1
        #self.id_meeting_owner = -1

        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
        # print("ALTERAR PARA HEROKU NA HORA DE DAR DEPLOY")
        # self.con = psycopg2.connect(user=data["Local_db"]["user"],
        #                             password=data["Local_db"]["password"],
        #                             host=data["Local_db"]["host"],
        #                             port=data["Local_db"]["port"],
        #                             database=data["Local_db"]["database"])

        self.db = DbInterface()
        # cria encontro
        if id_meeting is None:
            postgres_insert_query = """ INSERT INTO Encontro (IDMEETINGOWNER) VALUES (%s) RETURNING ID """
            cursor = self.con.cursor()
            cursor.execute(postgres_insert_query, (id_meeting_owner,))
            self.con.commit()
            self.id_meeting = cursor.fetchone()[0]
        else:
            self.id_meeting = id_meeting
        self.id_meeting_owner = id_meeting_owner

        # thread attributes
        threading.Thread.__init__(self)
        self.og = og.OutputGenerator()
        self.og.start()

        # negociate attributes
        self.event_queue = Queue()# Queue('~/temporary_state/' + str(self.id_meeting) + 'event_queue')
        self.output_queue = Queue() # Queue('~/temporary_state/' + str(self.id_meeting) + 'output_queue')
        self.request_queue = Queue() # Queue('~/temporary_state/' + str(self.id_meeting) + 'request_queue')
        self.request_state = None

        # selector
        self.dms = dms

        self.save_queue = False
        self.load_queue = False

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)

    def finish_fsm(self):
        print("\nnotificando todos os usuarios do cancelamento\n")
        for person in self.with_list:
            print("\nperson %s\n" % person)

    def finish_fsm_sucess(self):
        print("\nTODOS OS USUARIOS NOTIFICADOS!\n")
        self.dms.kill_dm(self.id_meeting)
        #self.reset()
        #return Idle('', self)
        #for person in self.with_list:
        #    print("person %s" % person)

    '''
    Resets dm to it's initial state
    '''
    def reset(self):
        print("remove")
        for id in self.with_list:
            del self.dms.users_active_meeting[id]
        # self.with_list = []
        # self.where = []
        # self.when = []
        # self.date = []
        # self.hour = []
        # self.commitment = []
        # self.income_data = []
        # self.event_queue = queue.Queue()
        # self.output_queue = queue.Queue()
        # self.id_meeting = -1
        # self.id_meeting_owner = -1


    def dispatch_msg(self, income_message):

        # process intentions
        # if income_message.intent != "":
        if income_message == 'save_queues':
            self.save_queue = True
            return
        elif income_message == 'load_queues':
            self.load_queue = True
            return

        self.income_data = income_message
        self.state.income_data = income_message
        # self.on_event(income_message.intent)
        if (income_message.intent):
            self.event_queue.put(income_message.intent)
        print("Mensagem recebida!  ")
        return

    def set_internal_event(self, income_message):
        # if self.state.hasInternalEvent is True:
            self.income_data = income_message
            self.state.income_data = income_message
            # self.on_event('internal_event')
            self.event_queue.put('internal_event')
            print("Evento interno enfileirado  ")
            return

    def set_event(self, event):
        self.event_queue.put(event)

    def run(self):
        while True:
            if self.save_queue:
                self.save_queues()
                self.save_queue = False
            if self.load_queue:
                self.load_queues()
                self.load_queue = False
            if self.event_queue.qsize() > 0:
                print("Evento disparado  ")
                self.on_event(self.event_queue.get())
            time.sleep(0.01)

    def send_output(self):
        if not self.output_queue.qsize() == 0:
            message = self.output_queue.get()
            self.dms.users_active_meeting[message.id_user] = self.id_meeting
            # Não me orgulho disso
            message.intent = [message.intent]
            if 'confirm' in message.intent or 'notify_initial_info' in message.intent \
                    or 'invite' in message.intent or 'notify_completed' in message.intent \
                    or 'notify_response_accept' in message.intent or 'notify_change_rejected' in message.intent \
                    or 'notify_change' in message.intent:
                msg = json.dumps(message.__dict__)
                self.og.dispatch_msg(msg)
                while not self.output_queue.qsize() == 0:
                    message = self.output_queue.get()
                    message.intent = [message.intent]
                    msg = json.dumps(message.__dict__)
                    self.dms.users_active_meeting[message.id_user] = self.id_meeting
                    self.og.dispatch_msg(msg)
                return
            # concatena intenções para realizar várias perguntas
            while not self.output_queue.qsize() == 0:
                item = self.output_queue.get()
                if item.intent == 'desambiguate':
                    if item.place_known != '':
                        message.place_known.append(item.place_known)
                    elif item.person_know != '':
                        for person in item.person_know:
                            message.person_know.append(person)
                message.intent.append(item.intent)

            msg = json.dumps(message.__dict__)
            print("Json saindo do DM: ", msg)
            self.og.dispatch_msg(msg)

    def notify_all_members(self, intent='confirm'):
        # finished, will notify all users in the meeting
        user_query = """SELECT IDCLIENTE from ListaEncontro WHERE IDENCONTRO = (%s) AND ACEITOU <> 2 """
        cur = self.con.cursor()
        cur.execute(user_query, (self.id_meeting,))
        clientes = cur.fetchall()
        for cliente in clientes:
            message = dialog_message.DialogMessage(intent, self.commitment, self.with_list, '', \
                                                   self.where, '', self.date, self.hour, '', \
                                                   cliente[0])  # criar meetingowner
            self.output_queue.put(message)
        self.send_output()
    '''
    Sends next request message for meeting owner
    '''
    def set_next_request(self):
        if not self.request_queue.qsize() == 0:
            income_data = self.request_queue.get()
            if 'excl_pessoa' in income_data.intent or 'add_pessoa' in income_data.intent:
                self.request_state = ChangeWithList(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], income_data.person_know,
                                                       income_data.person_unknown, '', '', '', '',
                                                       income_data.id_user, self.dm.id_meeting_owner)

                # self.set_event('change_withlist_internal')
            elif 'change_where' in income_data.intent:
                self.request_state = ChangeWhere(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '', '', income_data.place_known,
                                                       income_data.place_unknown, '', '',
                                                       income_data.id_user, self.id_meeting_owner)
                # self.set_event('change_where_intenal')
            elif 'change_date' in income_data.intent:
                self.request_state = ChangeDate(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '',
                                                       '', '', '', income_data.date, '',
                                                       income_data.id_user, self.id_meeting_owner)

                # self.set_event(['change_date_internal'])
            elif 'change_hour' in income_data.intent:
                self.request_state = ChangeHour(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '',
                                                       '', '', '', '', income_data.hour,
                                                       income_data.id_user, self.id_meeting_owner)

                # self.set_event(['change_hour_internal'])
            msg = json.dumps(message.__dict__)
            self.og.dispatch_msg(msg)
        else:
            self.request_state = None

    #def save_queues(self):
        # with open(str(self.id_meeting) + 'event_queue', 'wb') as dm_file:
            # pk.dump(self.event_queue, dm_file)
        # with open(str(self.id_meeting) + 'output_queue', 'wb') as dm_file:
            # pk.dump(self.output_queue, dm_file)
        # with open(str(self.id_meeting) + 'request_queue', 'wb') as dm_file:
            # pk.dump(self.request_queue, dm_file)
        # with open('~/temporary_state/' + str(self.id_meeting) + 'request_state', 'wb') as dm_file:
            # pk.dump(self.request_state.__name__, dm_file)
        # with open('~/temporary_state/' + str(self.id_meeting) + 'state', 'wb') as dm_file:
            # pk.dump(self.state.__name__, dm_file)

    # def load_queues(self):
    #     # with open(str(self.id_meeting) + 'event_queue', 'rb') as dm_file:
    #         # self.event_queue = pk.load(self.event_queue, dm_file)
    #     # with open(str(self.id_meeting) + 'output_queue', 'rb') as dm_file:
    #         # self.request_queue = pk.load(self.output_queue, dm_file)
    #     # with open(str(self.id_meeting) + 'request_queue', 'rb') as dm_file:
    #         # self.request_state = pk.load(self.request_queue, dm_file)
    #     #name_state_request = ""
    #     # with open('~/temporary_state/' +str(self.id_meeting) + 'request_state', 'rb') as dm_file:
    #         # self.request_state = pk.load(name_state_request, dm_file)
    #     name_state = ""
    #     with open('~/temporary_state/' + str(self.id_meeting) + 'state', 'rb') as dm_file:
    #         name_state = pk.load(dm_file)
    #     if name_state == 'Idle':
    #         self.state = Idle(None, self)
    #     elif name_state == 'InitialInfo':
    #         self.state = InitialInfo(self)
    #     elif name_state == 'InfoCompleted':
    #         self.state = InfoCompleted(self)
    #     #elif name_state is 'ChangeWhere':
    #         #self.state = ChangeWhere(self)
    #     else:
    #         self.state = Idle()
