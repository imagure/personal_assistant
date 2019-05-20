import ast
import json
import queue
import random
import threading
import time

from output_generator import MessageSender as msender

message_sender = msender.MessageSender()
message_sender.start()


class OutputGenerator(threading.Thread):

    ask_what = False
    ask_where = False
    ask_date = False
    ask_hour = False
    ask_withlist = False
    ask_who = False
    disambiguate = False

    notify_initial_info = False
    invite = False
    excl_person = False
    add_person = False
    change_place = False
    change_hour = False
    change_date = False

    notify_change_accepted = False
    notify_change_rejected = False

    notify_response_accept = False
    notify_response_reject = False

    notify_completed = False

    response = []
    people = []
    commitment = ""
    date = []
    hour = []
    place = ""
    id_request = ""

    def __init__(self):
        self.event_queue = queue.Queue()
        self.output_queue = queue.Queue()
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

    def find_user_id(self, income_data):
        return income_data["id_user"]

    def find_people(self):
        people = []
        for item in self.people:
            if type(item) == list:
                for list_item in item:
                    people.append(list_item)
            elif type(item) == str:
                people.append(item)
        self.people = people

    def find_intent(self, income_data):

        print("Income data: ", income_data)
        intents = income_data["intent"]
        self.people = list(income_data["person_know"])+list(income_data["person_unknown"])
        self.find_people()
        self.date = list(income_data["date"])
        self.hour = list(income_data["hour"])
        self.commitment = list(income_data["commitment"])
        self.place = list(income_data["place_known"])+list(income_data["place_unknown"])
        self.id_request = list(income_data["dont_know"])

        for intent in intents:
            if intent == 'ask_what':
                self.ask_what = True
            elif intent == 'ask_where':
                self.ask_where = True
            elif intent == 'ask_withlist':
                self.ask_withlist = True
            elif intent == 'ask_date':
                self.ask_date = True
            elif intent == 'ask_hour':
                self.ask_hour = True
            elif intent == 'ask_who':
                self.ask_who = True
            elif intent == 'desambiguate':
                self.disambiguate = True
            elif intent == 'notify_initial_info':
                self.notify_initial_info = True
            elif intent == 'invite':
                self.invite = True
            elif intent == 'add_pessoa':
                self.add_person = True
            elif intent == 'excl_pessoa':
                self.excl_person = True
            elif intent == 'change_place':
                self.change_place = True
            elif intent == 'change_hour':
                self.change_hour = True
            elif intent == 'change_date':
                self.change_date = True
            elif intent == 'notify_change_accepted':
                self.notify_change_accepted = True
            elif intent == 'notify_change_rejected':
                self.notify_change_rejected = True
            elif intent == 'notify_response_accept':
                self.notify_change_rejected = True
            elif intent == 'notify_response_reject':
                self.notify_change_rejected = True
            elif intent == 'notify_completed':
                self.notify_completed = True

    def reset(self):
        self.ask_date = False
        self.ask_hour = False
        self.ask_where = False
        self.ask_withlist = False
        self.ask_what = False
        self.ask_who = False
        self.disambiguate = False
        self.invite = False
        self.excl_person = False
        self.add_person = False
        self.change_place = False
        self.change_hour = False
        self.change_date = False
        self.notify_initial_info = False
        self.notify_change_accepted = False
        self.notify_change_rejected = False
        self.notify_response_accept = False
        self.notify_response_reject = False
        self.notify_completed = False
        self.response = []
        self.people = []

    def run(self):
        while True:
            if self.event_queue.qsize() > 0:
                print("Evento disparado  ")
                income_data = self.event_queue.get()
                self.find_intent(income_data)
                user_id = self.find_user_id(income_data)
                # print()
                self.send_output(user_id)
            time.sleep(0.01)

    def send_output(self, user_id):
        print("-" * 30)
        og_response = self.formulate_response()
        print(og_response)
        response_dict = {'text': og_response, 'user_id': user_id, 'is_new_user': 'false'}
        message_sender.dispatch_msg(response_dict)
        self.reset()
        print("-" * 30)

    def formulate_response(self):
        if self.ask_who:
            random_choice = random.choice(self.data["Outputs"]["ask_who"])
            self.response.append(random_choice)
        elif self.disambiguate:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_person"])
            names = self.data["conectors"][1].join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.invite:
            random_choice = random.choice(self.data["Outputs"]["invite"])
            names = self.data["conectors"][0].join(self.people)
            date = self.data["conectors"][2].join(self.date)
            hour = self.data["conectors"][1].join(self.hour)
            place = self.data["conectors"][1].join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)
        elif self.notify_initial_info:
            random_choice = random.choice(self.data["Outputs"]["notify_initial_info"])
            names = self.data["conectors"][0].join(self.people)
            date = self.data["conectors"][2].join(self.date)
            hour = self.data["conectors"][1].join(self.hour)
            place = self.data["conectors"][1].join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)

        elif self.excl_person:
            random_choice = random.choice(self.data["Outputs"]["excl_person"])
            names = self.data["conectors"][0].join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.add_person:
            random_choice = random.choice(self.data["Outputs"]["add_pessoa"])
            names = self.data["conectors"][0].join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.change_place:
            random_choice = random.choice(self.data["Outputs"]["change_place"])
            places = self.data["conectors"][0].join(self.place)
            text = random_choice.format(places)
            self.response.append(text)
        elif self.change_hour:
            random_choice = random.choice(self.data["Outputs"]["change_hour"])
            hours = self.data["conectors"][1].join(self.hour)
            text = random_choice.format(hours)
            self.response.append(text)
        elif self.change_date:
            random_choice = random.choice(self.data["Outputs"]["change_date"])
            dates = self.data["conectors"][1].join(self.date)
            text = random_choice.format(dates)
            self.response.append(text)
        elif self.notify_change_accepted:
            random_choice = random.choice(self.data["Outputs"]["notify_change_accepted"])
            names = self.data["conectors"][0].join(self.people)
            date = self.data["conectors"][2].join(self.date)
            hour = self.data["conectors"][1].join(self.hour)
            place = self.data["conectors"][1].join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)
        elif self.notify_change_rejected:
            random_choice = random.choice(self.data["Outputs"]["notify_change_rejected"])
            self.response.append(random_choice)

        elif self.notify_response_accept:
            random_choice = random.choice(self.data["Outputs"]["notify_response_accept"])
            name = self.people[0]
            text = random_choice.format(name)
            self.response.append(text)
        elif self.notify_response_reject:
            random_choice = random.choice(self.data["Outputs"]["notify_response_reject"])
            name = self.people[0]
            text = random_choice.format(name)
            self.response.append(text)

        elif self.notify_completed:
            random_choice = random.choice(self.data["Outputs"]["notify_completed"])
            names = self.data["conectors"][0].join(self.people)
            date = self.data["conectors"][2].join(self.date)
            hour = self.data["conectors"][1].join(self.hour)
            place = self.data["conectors"][1].join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)

        if not self.ask_what and not self.ask_where and not self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["no_return"])
            self.response.append(random_choice)

        elif self.ask_what and not self.ask_where and not self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and not self.ask_withlist\
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_where"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_withlist"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and not self.ask_withlist \
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and not self.ask_withlist \
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_hour"])
            self.response.append(random_choice)

        elif self.ask_what and self.ask_where and not self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_who"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and not self.ask_withlist \
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_date"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and not self.ask_withlist \
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_hour"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and self.ask_withlist \
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_where_who"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and not self.ask_withlist \
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date_where"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and not self.ask_withlist \
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_hour_where"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and self.ask_withlist \
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date_who"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and not self.ask_withlist \
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date_hour"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and self.ask_withlist \
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_who_hour"])
            self.response.append(random_choice)

        elif self.ask_what and self.ask_where and self.ask_withlist\
                and not self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_who"])
            self.response.append(random_choice)
        elif self.ask_what and self.ask_where and not self.ask_withlist\
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_date"])
            self.response.append(random_choice)
        elif self.ask_what and self.ask_where and not self.ask_withlist\
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_hour"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and self.ask_withlist\
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_date_who"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and not self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_date_hour"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and self.ask_withlist\
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_who_hour"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and self.ask_withlist\
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date_where_who"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and not self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_date_where_hour"])
            self.response.append(random_choice)
        elif not self.ask_what and not self.ask_where and self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_who_hour_date"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and self.ask_withlist\
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_who_where_hour"])
            self.response.append(random_choice)

        elif self.ask_what and self.ask_where and self.ask_withlist\
                and self.ask_date and not self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_who_date"])
            self.response.append(random_choice)
        elif self.ask_what and self.ask_where and self.ask_withlist\
                and not self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_who_hour"])
            self.response.append(random_choice)
        elif self.ask_what and self.ask_where and not self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_date_hour"])
            self.response.append(random_choice)
        elif self.ask_what and not self.ask_where and self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_date_who_hour"])
            self.response.append(random_choice)
        elif not self.ask_what and self.ask_where and self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_where_who_date_hour"])
            self.response.append(random_choice)

        elif self.ask_what and self.ask_where and self.ask_withlist\
                and self.ask_date and self.ask_hour:
            random_choice = random.choice(self.data["Outputs"]["ask_what_where_who_date_hour"])
            self.response.append(random_choice)

        return ' '.join(self.response)
