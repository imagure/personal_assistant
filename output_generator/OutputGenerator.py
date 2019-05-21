import ast
import json
import queue
import random
import threading

from output_generator import MessageSender as msender

message_sender = msender.MessageSender()


class OutputGenerator(threading.Thread):

    intents = []
    response = []
    people = []
    commitment = ""
    date = []
    hour = []
    place = ""
    id_request = ""

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
        self.event_queue.put(ast.literal_eval(income_message))

    def dispatch_new_user_msg(self, income_message):
        print("Adicionando", income_message)
        self.new_user_queue.put(income_message)

    def run(self):
        while True:

            if not self.event_queue.empty():
                income_data = self.event_queue.get()
                # message = dm_message.from_json(income_data)
                self._find_intent(income_data)
                self._find_entities(income_data)
                user_id = income_data["id_user"]
                response = self._formulate_response_old_user()
                response_dict = {'user_id': user_id,
                                 'text': response,
                                 'is_new_user': 'false'}
                self.send_output(response_dict)

            elif not self.new_user_queue.empty():
                income_data = self.new_user_queue.get()
                self._find_intent_new_user(income_data)
                self._find_entities_new_user(income_data)
                user_id = income_data.id_user
                response = self._formulate_response_new_user()
                response_dict = {'user_id': user_id,
                                 'text': response,
                                 'is_new_user': 'true'}
                self.send_output(response_dict)

    def _find_intent_new_user(self, income_data):

        self.intents = income_data.intent

    def _find_intent(self, income_data):

        self.intents = income_data["intent"]

    def _find_entities(self, income_data):
        self.people = list(income_data["person_know"]) + list(income_data["person_unknown"])
        self._find_people()
        self.date = list(income_data["date"])
        self.hour = list(income_data["hour"])
        self.commitment = list(income_data["commitment"])
        self.place = list(income_data["place_known"]) + list(income_data["place_unknown"])
        self.id_request = income_data["dont_know"]

    def _find_entities_new_user(self, income_data):
        self.people = income_data.person_known

    def _find_people(self):
        people = []
        for item in self.people:
            if type(item) == list:
                for list_item in item:
                    people.append(list_item)
            elif type(item) == str:
                people.append(item)
        self.people = people

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

    def _formulate_response_new_user(self):
        user_name = self.people
        if "new_user_wait" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_wait"])
            text = random_choice.format(user_name)
            self.response.append(text)
        elif "new_user_success" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_success"])
            text = random_choice.format(user_name)
            self.response.append(text)
        elif "new_user_insert_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_insert_fail"])
            text = random_choice.format(user_name)
            self.response.append(text)
        elif "new_user_contacts_slack_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_contacts_slack_fail"])
            text = random_choice.format(user_name)
            self.response.append(text)
        elif "new_user_contacts_db_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_contacts_db_fail"])
            text = random_choice.format(user_name)
            self.response.append(text)
        return ' '.join(self.response)

    def _formulate_response_old_user(self):
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
            info["names"] = self.data["conectors"][0].join(self.people)
        if self.place:
            info["place"] = self.data["conectors"][1].join(self.place)
        if self.date:
            info["date"] = self.data["conectors"][2].join(self.date)
        if self.hour:
            info["hour"] = self.data["conectors"][1].join(self.hour)
        return random_choice.format(info=info)
