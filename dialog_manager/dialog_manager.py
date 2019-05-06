from dialog_manager.dialog_manager_states import *
from dialog_message.dialog_message import *
import output_generator.OutputGenerator as og
import queue
import threading
import time
import json
import psycopg2

ask_list = {'ask_what', 'ask_when', 'ask_with', 'ask_withlist', 'ask_where'}

with open("configs/databases.json") as f:
    data = json.load(f)


class DialogManager(threading.Thread):
    def __init__(self):
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
        self.event_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.id_meeting = -1
        self.id_meeting_owner = -1

        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
        # print("ALTERAR PARA HEROKU NA HORA DE DAR DEPLOY")
        # self.con = psycopg2.connect(user="postgres",
        #                             password="Toalhamesa",
        #                             host="127.0.0.1",
        #                             port="5432",
        #                             database="dev")

        # thread attributes
        threading.Thread.__init__(self)
        self.og = og.OutputGenerator()
        self.og.start()

        # negociate attributes
        self.request_queue = queue.Queue()
        self.request_state = None

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
        self.reset()
        return Idle('', self)
        #for person in self.with_list:
        #    print("person %s" % person)

    '''
    Resets dm to it's initial state
    '''
    def reset(self):
        self.with_list = []
        self.where = []
        self.when = []
        self.date = []
        self.hour = []
        self.commitment = []
        self.income_data = []
        self.event_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.id_meeting = -1
        self.id_meeting_owner = -1

    def dispatch_msg(self, income_message):

        # process intentions
        # if income_message.intent != "":
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
            if self.event_queue.qsize() > 0:
                print("Evento disparado  ")
                self.on_event(self.event_queue.get())
            time.sleep(0.01)

    def send_output(self):
        if not self.output_queue.empty():
            message = self.output_queue.get()
            # Não me orgulho disso
            message.intent = [message.intent]
            if 'confirm' in message.intent:
                msg = json.dumps(message.__dict__)
                self.og.dispatch_msg(msg)
                while not self.output_queue.empty():
                    message = self.output_queue.get()
                    message.intent = [message.intent]
                    msg = json.dumps(message.__dict__)
                    self.og.dispatch_msg(msg)
                return
            if 'notify' in message.intent:
                msg = json.dumps(message.__dict__)
                self.og.dispatch_msg(msg)
                while not self.output_queue.empty():
                    message = self.output_queue.get()
                    message.intent = [message.intent]
                    msg = json.dumps(message.__dict__)
                    self.og.dispatch_msg(msg)
                return
            # concatena intenções para realizar várias perguntas
            while not self.output_queue.empty():
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
        if not self.request_queue.empty():
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
