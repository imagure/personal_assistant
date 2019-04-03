import random
import json
import ast
import queue
import threading
import time
from output_generator import message_sender as msender

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
    confirm = False
    excl_person = False
    add_person = False
    change_place = False
    change_hour = False
    change_date = False
    change_refused = False
    confirm_new_info = False
    notify = False
    response = []
    people = []
    commitment = ""
    date = []
    hour = []
    place = ""

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

    def find_intent(self, income_data):
        print("Income data: ", income_data)
        intents = income_data["intent"] #.split(" ") # se virar vetor, remover
        self.people = list(income_data["person_know"])+list(income_data["person_unknown"])
        self.date = list(income_data["date"])
        self.hour = list(income_data["hour"])
        self.commitment = list(income_data["commitment"])
        self.place = list(income_data["place_known"])+list(income_data["place_unknown"])
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
            elif intent == 'desambiguate':
                self.disambiguate = True
            elif intent == 'ask_who':
                self.ask_who = True
            elif intent == 'confirm':
                self.confirm = True
            elif intent == 'add_pessoa':
                self.add_person = True
            elif intent == 'excl_pessoa':
                self.excl_person = True
            elif intent == 'mudar_lugar':
                self.change_place = True
            elif intent == 'confirm_new_info':
                self.confirm_new_info = True
            elif intent == 'change_hour':
                self.change_hour = True
            elif intent == 'change_date':
                self.change_date = True
            elif intent == 'change_refused':
                self.change_refused = True
            elif intent == 'notify':
                self.notify = True

    def reset(self):
        self.ask_date = False
        self.ask_hour = False
        self.ask_where = False
        self.ask_withlist = False
        self.ask_what = False
        self.ask_who = False
        self.disambiguate = False
        self.confirm = False
        self.excl_person = False
        self.add_person = False
        self.change_place = False
        self.confirm_new_info = False
        self.change_hour = False
        self.change_date = False
        self.change_refused = False
        self.notify = False
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
        response_dict = {'text': og_response, 'user_id': user_id}
        message_sender.dispatch_msg(response_dict)
        self.reset()
        print("-" * 30)

    def formulate_response(self):
        if self.ask_who:
            random_choice = random.choice(self.data["Outputs"]["ask_who"])
            self.response.append(random_choice)
        elif self.notify:
            random_choice = random.choice(self.data["Outputs"]["notify"])
            self.response.append(random_choice)
        elif self.disambiguate:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_person"])
            names = ' ou '.join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.confirm:
            random_choice = random.choice(self.data["Outputs"]["confirm"])
            names = ' e '.join(self.people)
            date = ' à '.join(self.date)
            hour = ' ou '.join(self.hour)
            place = ' ou '.join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)
        elif self.confirm_new_info:
            random_choice = random.choice(self.data["Outputs"]["confirm_new_info"])
            names = ' e '.join(self.people)
            date = ' à '.join(self.date)
            hour = ' ou '.join(self.hour)
            place = ' ou '.join(self.place)
            commitment = '/'.join(self.commitment)
            text = random_choice.format(commitment, date, hour, names, place)
            self.response.append(text)
        elif self.excl_person:
            random_choice = random.choice(self.data["Outputs"]["excl_person"])
            names = ' e '.join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.add_person:
            random_choice = random.choice(self.data["Outputs"]["add_pessoa"])
            names = ' e '.join(self.people)
            text = random_choice.format(names)
            self.response.append(text)
        elif self.change_place:
            random_choice = random.choice(self.data["Outputs"]["change_place"])
            places = ' e '.join(self.place)
            text = random_choice.format(places)
            self.response.append(text)
        elif self.change_hour:
            random_choice = random.choice(self.data["Outputs"]["change_hour"])
            hours = ' ou '.join(self.hour)
            text = random_choice.format(hours)
            self.response.append(text)
        elif self.change_date:
            random_choice = random.choice(self.data["Outputs"]["change_date"])
            dates = ' ou '.join(self.date)
            text = random_choice.format(dates)
            self.response.append(text)
        elif self.change_refused:
            random_choice = random.choice(self.data["Outputs"]["change_refused"])
            self.response.append(random_choice)

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
