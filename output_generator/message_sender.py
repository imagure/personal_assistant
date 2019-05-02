import queue
import threading

from client_interface.slack_client import SlackHelper
from db.db_interface import db_interface

db_interface = db_interface()


class MessageSender(threading.Thread):

    def __init__(self):
        self.input_queue = queue.Queue()
        self.id = None
        self.input_queue = queue.Queue()
        self.slack = SlackHelper()
        threading.Thread.__init__(self)

    def dispatch_msg(self, msg):
        self.input_queue.put(msg)

    def run(self):
        while True:
            self.send_output()

    def send_output(self):
        if not self.input_queue.empty():
            response_dict = self.input_queue.get()
            user_id = response_dict["user_id"]
            response_text = response_dict["text"]
            if response_dict["existance"] == 'true':
                channel_id = db_interface.search_contact(user_id=user_id)
                self.slack.post_msg(response_text, channel_id)
            elif response_dict["existance"] == 'false':
                channel_id = user_id
                self.slack.post_msg(response_text, channel_id)
