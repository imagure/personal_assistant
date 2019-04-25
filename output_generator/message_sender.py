import queue
import threading
import json
import psycopg2
from slackclient import SlackClient

slack_token = "xoxp-594442784566-594078665495-594140143367-1ab73b6dc2af6708e8491518ff515091"
sc = SlackClient(slack_token)

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
            print(channel_id)
            self.send_slack(response_text, channel_id)

    def send_slack(self, response, channel_id):
        sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=response
        )
