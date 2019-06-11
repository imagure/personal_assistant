import json


class NewUserDialogMessage(object):

    def __init__(self, intent, person_known, id_user, team_id):
        self.intent = intent
        self.person_known = person_known
        self.id_user = id_user
        self.team_id = team_id

    @classmethod
    def from_json(cls, json_message):

        json_dict = json.loads(json_message)
        if json_dict["intent"]:
            intent = [json_dict["intent"]]
        else:
            intent = []

        if json_dict["person_known"]:
            person_known = [json_dict["person_known"]]
        else:
            person_known = []

        if json_dict["id_user"]:
            id_user = json_dict['id_user']
        else:
            id_user = []

        if json_dict["team_id"]:
            team_id = json_dict['team_id']
        else:
            team_id = []

        return cls(intent, person_known, id_user, team_id)
