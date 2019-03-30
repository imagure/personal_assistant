import json


class ModeManager:

    def __init__(self):
        self.mode = None

    def which_mode(self, json_message):
        json_dict = json.loads(json_message)
        if 'mode' in json_dict:
            self.mode = json_dict["mode"]
        else:
            self.mode = "regular"

        return self.mode
