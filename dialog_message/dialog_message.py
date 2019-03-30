import json


class DialogMessage(object):
    with_list = {}
    place = ""
    intent = ""
    date = ""
    hour = ""
    dont_know = ""

    def __init__(self, intent, commitment, person_known, person_unknown,
                 place_known, place_unknown, date, hour, dont_know, id_user):
        self.intent = intent
        self.commitment = commitment
        self.person_know = person_known
        self.person_unknown = person_unknown
        self.place_known = place_known
        self.place_unknown = place_unknown
        self.date = date
        self.hour = hour
        self.dont_know = dont_know
        self.id_user = id_user

    @classmethod
    def from_json(cls, json_message):

        # works as
        # self.with_list = {json_dict["with_list"]}
        # self.place = json_dict["place"]
        # self.intent = json_dict["intent"]
        # self.date = json_dict["date"]
        # self.hour = json_dict["hour"]
        # self.dont_know = json_dict["dont_know"]
        json_dict = json.loads(json_message)
        if 'intent' in json_dict:
            intent = json_dict["intent"]
        else:
            intent = ""
        if 'commitment' in json_dict:
            commitment = json_dict["commitment"]
        else:
            commitment = ""
        if 'person_known' in json_dict:
            person_known = json_dict["person_known"]
        else:
            person_known = ""
        if 'person_unknown' in json_dict:
            person_unknown = json_dict['person_unknown']
        else:
            person_unknown = ""
        if 'place_known' in json_dict:
            place_known = json_dict['place_known']
        else:
            place_known = ""
        if 'place_unknown' in json_dict:
            place_unknown = json_dict['place_unknown']
        else:
            place_unknown = ""
        if 'date' in json_dict:
            date = json_dict['date']
        else:
            date = ""
        if 'hour' in json_dict:
            hour = json_dict['hour']
        else:
            hour = ""
        if 'dont_know' in json_dict:
            dont_know = json_dict['dont_know']
        else:
            dont_know = ""
        if 'id_user' in json_dict:
            id_user = int(json_dict['id_user'])
        else:
            id_user = ""

        return cls(intent, commitment, person_known, person_unknown,
                   place_known, place_unknown, date, hour, dont_know, id_user)
