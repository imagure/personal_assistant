import json


class SelectorMessage(object):

    def __init__(self, intent, meeting_info, id_user):
        self.intent = intent
        self.meeting_data = meeting_info
        self.id_user = id_user

    def __str__(self):
        print(self.intent)
        print(self.meeting_data)
        print(self.id_user)
        return "fim"

    @classmethod
    def from_json(cls, json_message):

        json_dict = json.loads(json_message)
        if json_dict["intent"]:
            intent = json_dict["intent"]
        else:
            intent = []

        if json_dict["meeting_data"]:
            meeting_data = json_dict['meeting_data']
        else:
            meeting_data = []

        if json_dict["id_user"]:
            id_user = json_dict['id_user']
        else:
            id_user = []

        return cls(intent, meeting_data, id_user)
