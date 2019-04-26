import json
import queue
import threading

import psycopg2

from client_interface.slack_client import SlackHelper

with open("configs/databases.json") as f:
    data = json.load(f)


class MessageSender(threading.Thread):

    def __init__(self):
        self.input_queue = queue.Queue()
        self.id = None
        self.input_queue = queue.Queue()
        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
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
            channel_id = response_dict["user_id"]
            response_text = response_dict["text"]
            if response_dict["existance"] == 'true':
                query = """SELECT FORMACONTATO FROM USUARIO WHERE ID = (%s)"""
                cursor = self.con.cursor()
                cursor.execute(query, (channel_id,))
                channel_id = cursor.fetchall()[0][0]
            self.slack.post_msg(response_text, channel_id)
