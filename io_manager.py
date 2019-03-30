from semanticizer.Semanticizer import Semanticizer
from dialog_manager.dialog_manager import DialogManager
from dialog_message.dialog_message import *
import queue
import threading
import os
import psycopg2
from slackclient import SlackClient

slack_token = "xoxp-594442784566-594078665495-594140143367-1ab73b6dc2af6708e8491518ff515091"
sc = SlackClient(slack_token)
dm = DialogManager()
dm.start()
semanticizer = Semanticizer('regular', 'pt')

with open("configs/databases.json") as f:
    data = json.load(f)


class IOManager(threading.Thread):

    def __init__(self):
        self.input_queue = queue.Queue()
        self.id = None
        self.output_queue = queue.Queue()
        self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
                                    password=data["Heroku_db"]["password"],
                                    host=data["Heroku_db"]["host"],
                                    port=data["Heroku_db"]["port"],
                                    database=data["Heroku_db"]["database"])
        threading.Thread.__init__(self)

    def dispatch_msg(self, msg):
        self.input_queue.put(msg)

    def dispatch_channel(self, channel_id):
        query = """SELECT ID FROM USUARIO WHERE FORMACONTATO = (%s)"""
        cursor = self.con.cursor()
        cursor.execute(query, (channel_id, ))
        self.id = cursor.fetchall()[0][0]

    def run(self):
        while True:
            if not self.input_queue.empty():
                if self.id is not None:
                    msg = self.input_queue.get()
                    my_json = semanticizer.semantize(msg)
                    message = DialogMessage.from_json(my_json)
                    message.id_user = self.id
                    dm.dispatch_msg(message)
                    response = dm.og.get_response()
                    self.output_queue.put(response)
                    self.send_output()
                    self.id = None

    def send_output(self):
        if not self.output_queue.empty():
            response_dict = self.output_queue.get()
            channel_id = response_dict["user_id"]
            response_text = response_dict["text"]
            query = """SELECT FORMACONTATO FROM USUARIO WHERE ID = (%s)"""
            cursor = self.con.cursor()
            cursor.execute(query, (channel_id,))
            channel_id = cursor.fetchall()[0][0]
            self.send_slack(response_text, channel_id)

    def send_slack(self, response, channel_id):
        sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=response
        )
