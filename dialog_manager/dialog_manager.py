import threading
from queue import PriorityQueue, Queue

from db.sql.db_interface import *
from dialog_manager.dialog_manager_states import *
# from priorityq import PQ

ask_list = {'ask_what', 'ask_when', 'ask_with', 'ask_withlist', 'ask_where'}

with open("configs/databases.json") as f:
    data = json.load(f)


class EventData(object):
    def __init__(self, event, income_message, priority):
        self.event = event
        self.income_message = income_message
        self.priority = priority

    def __cmp__(self, another):
        if self.priority > another.priority :
            return 1
        elif self.priority < another.priority:
            return -1
        return 0


class DialogManager(threading.Thread):
    def __init__(self, id_meeting_owner, dms, og, id_meeting=None):
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

        # self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
        #                             password=data["Heroku_db"]["password"],
        #                             host=data["Heroku_db"]["host"],
        #                             port=data["Heroku_db"]["port"],
        #                             database=data["Heroku_db"]["database"])
        print("ALTERAR PARA HEROKU NA HORA DE DAR DEPLOY")
        self.con = psycopg2.connect(user=data["Local_db"]["user"],
                                    password=data["Local_db"]["password"],
                                    host=data["Local_db"]["host"],
                                    port=data["Local_db"]["port"],
                                    database=data["Local_db"]["database"])

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
        self.og = og


        # negociate attributes
        self.event_queue = PriorityQueue()  #Queue('~/temporary_state/' + str(self.id_meeting) + 'event_queue')
        self.output_queue = Queue()  # Queue('~/temporary_state/' + str(self.id_meeting) + 'output_queue')
        self.request_queue = Queue()  # Queue('~/temporary_state/' + str(self.id_meeting) + 'request_queue')
        self.selector_queue = Queue()
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

    def finish_fsm_sucess(self):
        print("\nTODOS OS USUARIOS NOTIFICADOS!\n")
        self.dms.kill_dm(self.id_meeting)
        self.state = End()

    '''
    Resets dm to it's initial state
    '''
    #def reset(self):
    #    print("remove")
    #    for id in self.with_list:
    #        del self.dms.users_active_meeting[id]

    def dispatch_msg(self, income_message):
        self.event_queue.put(EventData(income_message.intent, income_message, 1))
        return

    def set_internal_event(self, income_message):
            self.event_queue.put(EventData('internal_event', income_message, 0))
            print("Evento interno enfileirado  ")
            return

    def set_event(self, event):
        self.event_queue.put(EventData(event, None, 0))

    def run(self):
        while True:
            if self.event_queue.qsize() > 0:
                print("Evento disparado  ")
                event_data = self.event_queue.get()
                if event_data.income_message is not None:
                    self.income_data = event_data.income_message
                    self.state.income_data = event_data.income_message
                self.on_event(event_data.event)
            if self.selector_queue.qsize() > 0:
                self.notify_all_members_from_selector(self.selector_queue.get())
            # time.sleep(0.001)

    def send_output(self):
        if not self.output_queue.qsize() == 0:
            message = self.output_queue.get()
            self.dms.users_active_meeting[message.id_user] = self.id_meeting
            # Não me orgulho disso
            if type(message.intent) is not list:
                message.intent = [message.intent]
            if 'confirm' in message.intent or 'notify_initial_info' in message.intent \
                    or 'invite' in message.intent or 'notify_completed' in message.intent \
                    or 'notify_response_accept' in message.intent or 'notify_change_rejected' in message.intent \
                    or 'notify_change' in message.intent or "notify_revival" in message.intent:
                msg = json.dumps(message.__dict__)
                self.og.dispatch_msg(msg)
                while not self.output_queue.qsize() == 0:
                    message = self.output_queue.get()
                    if type(message.intent) is not list:
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

    def notify_all_members_selector(self, intent, data=None):
        message = {"intent": intent,
                   "data": data}
        self.selector_queue.put(message)

    def notify_all_members_from_selector(self, message):
        intent = message["intent"]
        data = message["data"]
        # finished, will notify all users in the meeting
        user_query = """SELECT IDCLIENTE from ListaEncontro WHERE IDENCONTRO = (%s) AND ACEITOU <> 2 """
        cur = self.con.cursor()
        cur.execute(user_query, (self.id_meeting,))
        clientes = cur.fetchall()
        for cliente in clientes:
            message = dialog_message.DialogMessage(intent, self.commitment, self.id_meeting_owner, '', \
                                                   data.place_unknown, '', data.date, data.hour, '', \
                                                   cliente[0])  # criar meetingowner
            self.output_queue.put(message)
        self.send_output()

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
                                                       income_data.id_user, self.id_meeting_owner)

            elif 'change_where' in income_data.intent:
                self.request_state = ChangeWhere(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '', '', income_data.place_known,
                                                       income_data.place_unknown, '', '',
                                                       income_data.id_user, self.id_meeting_owner)
            elif 'change_date' in income_data.intent:
                self.request_state = ChangeDate(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '',
                                                       '', '', '', income_data.date, '',
                                                       income_data.id_user, self.id_meeting_owner)

            elif 'change_hour' in income_data.intent:
                self.request_state = ChangeHour(self, income_data)
                message = dialog_message.DialogMessage(income_data.intent, [''], '',
                                                       '', '', '', '', income_data.hour,
                                                       income_data.id_user, self.id_meeting_owner)

            msg = json.dumps(message.__dict__)
            self.og.dispatch_msg(msg)
        else:
            self.request_state = None
