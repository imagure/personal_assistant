import json
import queue
import random
import threading

from output_generator import MessageSender as msender
from dialog_message import dm_message
from dialog_message import new_user_message
from db.sql.db_interface import DbInterface

message_sender = msender.MessageSender()
db_interface = DbInterface()


class OutputGenerator(threading.Thread):

    intents = []
    response = []
    people = []
    people_unknown = []
    commitment = ""
    date = []
    hour = []
    place = ""
    meeting_data = []
    specific_person = []
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
                                 'team_id': income_data.team_id,
                                 'is_new_user': 'true'}
                self.send_output(response_dict)

    def _find_info(self, income_data):

        if type(income_data) is dm_message.DM_Message:
            self.intents = income_data.intent
            self.commitment = income_data.commitment
            self.people = self._find_people_names(income_data.person_known)
            self.people_unknown = income_data.person_unknown
            self.place = income_data.place_known + income_data.place_unknown
            self.date = income_data.date
            self.hour = income_data.hour
            self.user_id = income_data.id_user
            self.specific_person = self._find_people_names(income_data.dont_know)
            self.meeting_data = income_data.message_data

        elif type(income_data) is new_user_message.NewUserDialogMessage:
            self.intents = income_data.intent
            self.people = income_data.person_known
            self.user_id = income_data.id_user

    def _find_people_names(self, people_ids):
        if type(people_ids) is list:
            return db_interface.search_users_names(people_ids)
        else:
            return db_interface.search_users_names([people_ids])

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
        self.people_unknown = []
        self.commitment = ""
        self.date = []
        self.hour = []
        self.place = ""
        self.specific_person = []
        self.user_id = ""

    def _formulate_response(self):

        if "wait_for_response" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["wait_for_response"])
            self.response.append(random_choice)
        elif "mo_occupied" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["mo_occupied"])
            self.response.append(random_choice)
        elif "mo_msg_received" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["mo_msg_received"])
            self.response.append(random_choice)
        elif "sorry_msg" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["sorry_msg"])
            self.response.append(random_choice)

        if "new_user_request_first_name" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_request_first_name"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_request_last_name" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_request_last_name"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_request_valid_name" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["new_user_request_valid_name"])
            text = self._format_message(random_choice)
            self.response.append(text)
        elif "new_user_wait" in self.intents:
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
            text = self._format_message(random_choice)
            self.response.append(text)

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

        if "notify_revival" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_revival"])
            text = self._format_message(random_choice)
            self.response.append(text)

        if "notify_new_state" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_new_state"])
            text = self._format_message(random_choice)
            self.response.append(text)

        if "excl_pessoa" in self.intents:
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

        elif "change_date_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["change_date_hour"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "change_place_selector" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["change_place_selector"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "add_person_selector" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["add_person_selector"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "excl_person_selector" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["excl_person_selector"])
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

        elif "notify_user_cancel" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_user_cancel"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_meeting_cancel" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_meeting_cancel"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "notify_change_accepted" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_change_accepted"])
            self.response.append(random_choice)

        elif "notify_change_rejected" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_change_rejected"])
            self.response.append(random_choice)

        elif "notify_response_accept" in self.intents:
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

        if "disambiguate_meeting" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_meeting"])
            text = self._format_message(random_choice)
            self.response.append(text)

        elif "disambiguate_withlist_where_date_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_withlist_where_date_hour"])
            self.response.append(random_choice)

        elif "disambiguate_where_date_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_where_date_hour"])
            self.response.append(random_choice)

        elif "disambiguate_date_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_date_hour"])
            self.response.append(random_choice)

        elif "disambiguate_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["disambiguate_hour"])
            self.response.append(random_choice)

        elif "notify_request_fail" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_request_fail"])
            self.response.append(random_choice)

        if "notify_found_meeting" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["notify_found_meeting"])
            self.response.append(random_choice)

        if "request_intent" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_intent"])
            self.response.append(random_choice)

        elif "request_new_place" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_new_place"])
            self.response.append(random_choice)

        elif "request_new_date_hour" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_new_date_hour"])
            self.response.append(random_choice)

        elif "request_add_person" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_add_person"])
            self.response.append(random_choice)

        elif "request_excl_person" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_excl_person"])
            self.response.append(random_choice)

        elif "request_cancel_meeting" in self.intents:
            random_choice = random.choice(self.data["Outputs"]["request_cancel_meeting"])
            self.response.append(random_choice)

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
                "names_un": "",
                "place": "",
                "date": "",
                "hour": "",
                "specific_person": "",
                "meeting": ""
                }
        if self.commitment:
            info["commitment"] = '/'.join(self.commitment)
        if self.people:
            if "desambiguate" in self.intents:
                info["names"] = self.data["conectors"][1].join(map(str, self.people))
            else:
                info["names"] = self.data["conectors"][0].join(map(str, self.people))
        if self.people_unknown:
            info["names_un"] = self.data["conectors"][0].join(map(str, self.people_unknown))
        if self.place:
            info["place"] = self.data["conectors"][1].join(self.place)
        if self.date:
            info["date"] = self.data["conectors"][2].join(self.date)
        if self.hour:
            info["hour"] = self.data["conectors"][1].join(self.hour)
        if self.specific_person:
            info["specific_person"] = self.data["conectors"][0].join(self.specific_person)
        if self.meeting_data:
            print(self.meeting_data)
            aux = []
            for data in self.meeting_data:
                data[0][0] = db_interface.search_users_names([data[0][0]])
                aux.append(self.data["meeting"].format(info=data[0]))
            print(aux)
            info["meeting"] = self.data["conectors"][1].join(aux)
        return random_choice.format(info=info)
