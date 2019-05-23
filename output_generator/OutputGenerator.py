import json
import queue
import random
import threading

from output_generator import MessageSender as msender
from dialog_message import dm_message
from dialog_message import new_user_message

message_sender = msender.MessageSender()


class OutputGenerator(threading.Thread):

    intents = []
    response = []
    people = []
    commitment = ""
    date = []
    hour = []
    place = ""
    user_id = ""

    def __init__(self):
        self.event_queue = queue.Queue()
        self.new_user_queue = queue.Queue()
        self.data = None
        threading.Thread.__init__(self)

    def set_language(self, language):
        if language == 'pt':
            with open("configs/output_phrases_pt.json") as f:
                self.data = json.load(f)
        elif language == 'en':
            with open("configs/output_phrases_en.json") as f:
                self.data = json.load(f)

    def dispatch_msg(self, income_message):
        print("Adicionando", income_message)
        self.event_queue.put(income_message)

    def dispatch_new_user_msg(self, income_message):
        print("Adicionando", income_message)
        self.new_user_queue.put(income_message)

    def run(self):
        while True:

            if not self.event_queue.empty():
                income_json = self.event_queue.get()
                income_data = dm_message.DM_Message.from_json(income_json)
                self._find_info(income_data)
                response = self._formulate_response()
                response_dict = {'user_id': self.user_id,
                                 'text': response,
                                 'is_new_user': 'false'}
                self.send_output(response_dict)

            elif not self.new_user_queue.empty():
                income_data = self.new_user_queue.get()
                self._find_info(income_data)
                response = self._formulate_response()
                response_dict = {'user_id': self.user_id,
                                 'text': response,
                                 'is_new_user': 'true'}
                self.send_output(response_dict)

    def _find_info(self, income_data):

        if type(income_data) is dm_message.DM_Message:
            self.intents = income_data.intent
            self.commitment = income_data.commitment
            self.people = income_data.person_known + income_data.person_unknown
            self.place = income_data.place_known + income_data.place_unknown
            self.date = income_data.date
            self.hour = income_data.hour
            self.user_id = income_data.id_user

        elif type(income_data) is new_user_message.NewUserDialogMessage:
            self.intents = income_data.intent
            self.people = income_data.person_known
            self.user_id = income_data.id_user

    def send_output(self, response_dict):
        print("-" * 30)
        print(response_dict["text"])
        print("-" * 30)
        message_sender.send_output(response_dict)
        self.reset()

    def reset(self):
        self.intents = []
        self.response = []
        self.people = []
        self.commitment = ""
        self.date = []
        self.hour = []
        self.place = ""
        self.user_id = ""

    def _formulate_response(self):

        if "new_user_wait" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_wait"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_success" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_success"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_insert_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_insert_fail"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_contacts_slack_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_contacts_slack_fail"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_contacts_db_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_contacts_db_fail"])
            text = self._format_message(random_choice)
            self.response.append(text)

        if "ask_who" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["ask_who"])
            self.response.append(random_choice)

        elif "desambiguate" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_person"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "invite" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["invite"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_initial_info" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_initial_info"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "excl_pessoa" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["excl_pessoa"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "add_pessoa" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["add_pessoa"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "change_place" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["change_place"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "change_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["change_hour"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "change_date" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["change_date"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_change_accepted" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_change_accepted"])
            self.response.append(random_choice)

        elif "notify_change_rejected" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_change_rejected"])
            self.response.append(random_choice)

        elif "notify_change_accept" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_response_accept"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_response_reject" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_response_reject"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_completed" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_completed"])
            text = self._format_message(random_choice)
            self.response.append(text)

        answer = ""
        if "ask_what" in self.intents:
            answer += "what_"
        if "ask_withlist" in self.intents:
            answer += "withlist_"
        if "ask_where" in self.intents:
            answer += "where_"
        if "ask_date" in self.intents:
            answer += "date_"
        if "ask_hour" in self.intents:
            answer += "hour_"
        if answer:
            text = random.choice(self.data["Outputs"][answer])
            self.response.append(text)

        return ' '.join(self.response)

    def _format_message(self, random_choice):
        info = {"commitment": "",
                "names": "",
                "place": "",
                "date": "",
                "hour": ""
                }
        if self.commitment:
            info["commitment"] = '/'.join(self.commitment)
        if self.people:
            info["names"] = self.data["conectors"][0].join(map(str, self.people))
        if self.place:
            info["place"] = self.data["conectors"][1].join(self.place)
        if self.date:
            info["date"] = self.data["conectors"][2].join(self.date)
        if self.hour:
            info["hour"] = self.data["conectors"][1].join(self.hour)
        return random_choice.format(info=info)
