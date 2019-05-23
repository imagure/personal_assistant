import json


class DM_Message(object):

    def __init__(self, intent, commitment, person_known, person_unknown,
                 place_known, place_unknown, date, hour, dont_know, id_user):
        self.intent = intent
        self.commitment = commitment
        self.person_known = person_known
        self.person_unknown = person_unknown
        self.place_known = place_known
        self.place_unknown = place_unknown
        self.date = date
        self.hour = hour
        self.dont_know = dont_know
        self.id_user = id_user

    @classmethod
    def from_json(cls, json_message):

        json_dict = json.loads(json_message)
        if json_dict["intent"]:
            intent = json_dict["intent"]
        else:
            intent = []

        if json_dict["commitment"]:
            commitment = json_dict["commitment"]
        else:
            commitment = []

        if json_dict["person_know"]:
            person_know = json_dict["person_know"]
            person_known = []
            for item in person_know:
                if type(item) == list:
                    for list_item in item:
                        person_known.append(list_item)
                elif type(item) == str:
                    person_known.append(item)
        else:
            person_known = []

        if json_dict["person_unknown"]:
            person_unknown = json_dict['person_unknown']
        else:
            person_unknown = []

        if json_dict["place_known"]:
            place_known = json_dict['place_known']
        else:
            place_known = []

        if json_dict["place_unknown"]:
            place_unknown = json_dict['place_unknown']
        else:
            place_unknown = []

        if json_dict["date"]:
            date = json_dict['date']
        else:
            date = []

        if json_dict["hour"]:
            hour = json_dict['hour']
        else:
            hour = []

        if json_dict["dont_know"]:
            dont_know = json_dict['dont_know']
        else:
            dont_know = []

        if json_dict["id_user"]:
            id_user = json_dict['id_user']
        else:
            id_user = []

        return cls(intent, commitment, person_known, person_unknown,
                   place_known, place_unknown, date, hour, dont_know, id_user)
