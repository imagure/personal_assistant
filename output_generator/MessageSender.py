from client_interface.slack_client import SlackHelper
from db.sql.db_interface import DbInterface

db_interface = DbInterface()


class MessageSender(object):

    def __init__(self):
        self.slack = SlackHelper()

    def send_output(self, response_dict):
        user_id = response_dict["user_id"]
        response_text = response_dict["text"]

        if response_dict["is_new_user"] == 'false':
            channel_id = db_interface.search_contact(user_id=user_id)
            self.slack.post_msg(response_text, channel_id)

        elif response_dict["is_new_user"] == 'true':
            channel_id = user_id
            self.slack.post_msg(response_text, channel_id)
