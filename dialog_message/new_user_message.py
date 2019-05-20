import json


class NewUserDialogMessage(object):
    with_list = {}
    place = ""
    intent = ""
    date = ""
    hour = ""
    dont_know = ""

    def __init__(self, intent, person_known, id_user):
        self.intent = intent
        self.person_known = person_known
        self.id_user = id_user

    @classmethod
    def from_json(cls, json_message):

        json_dict = json.loads(json_message)
        if 'intent' in json_dict:
            intent = json_dict["intent"]
        else:
            intent = ""
        if 'person_known' in json_dict:
            person_known = json_dict["person_known"]
        else:
            person_known = ""
        if 'id_user' in json_dict:
            id_user = json_dict['id_user']
        else:
            id_user = ""

        return cls(intent, person_known, id_user)
