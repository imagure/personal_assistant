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
        if 'intent' in json_dict:
            intent = json_dict["intent"]
        else:
            intent = ""

        if 'commitment' in json_dict:
            commitment = json_dict["commitment"]["value"]
        else:
            commitment = ""

        if 'person_know' in json_dict:
            person_know = json_dict["person_know"]
            person_known = []
            for item in person_know:
                if type(item) == list:
                    for list_item in item:
                        person_known.append(list_item)
                elif type(item) == str:
                    person_known.append(item)
        else:
            person_known = ""

        if 'person_unknown' in json_dict:
            person_unknown = json_dict['person_unknown']["value"]
        else:
            person_unknown = ""

        if 'place_known' in json_dict:
            place_known = json_dict['place_known']["value"]
        else:
            place_known = ""

        if 'place_unknown' in json_dict:
            place_unknown = json_dict['place_unknown']["value"]
        else:
            place_unknown = ""

        if 'date' in json_dict:
            date = json_dict['date']["value"]
        else:
            date = ""

        if 'hour' in json_dict:
            hour = json_dict['hour']["value"]
        else:
            hour = ""

        if 'dont_know' in json_dict:
            dont_know = json_dict['dont_know']["value"]
        else:
            dont_know = ""

        if 'id_user' in json_dict:
            id_user = json_dict['id_user']
        else:
            id_user = ""

        return cls(intent, commitment, person_known, person_unknown,
                   place_known, place_unknown, date, hour, dont_know, id_user)
