import os

from Crypto.Cipher import DES
from slackclient import SlackClient

from db.sql.db_interface import DbInterface

db_seed = os.environ["db_seed"]
des = DES.new(db_seed, DES.MODE_ECB)
db_interface = DbInterface()


class SlackHelper(object):

    @staticmethod
    def post_msg(response, channel_id, team_id=None):
        token = des.decrypt(bytes(db_interface.search_slack_workspace(team_id)))
        token = token[0:-4].decode('utf-8')
        # print("token here: ", token)  # tirar esse print
        client1 = SlackClient(token)
        client1.api_call(
            "chat.postMessage",
            username="PersonalAssistant",
            channel=channel_id,
            as_user=False,
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/"
                     "Mr._Smiley_Face.svg/2000px-Mr._Smiley_Face.svg.png",
            text=response
        )

    @staticmethod
    def find_user_channel(user_id, team_id):
        token = des.decrypt(bytes(db_interface.search_slack_workspace(team_id)))
        token = token[0:-4].decode('utf-8')
        # print("token here: ", token)  #tirar esse print
        client1 = SlackClient(token)
        user_channel = client1.api_call("conversations.open", users=user_id)
        print(user_channel)
        return user_channel["channel"]["id"]

    @staticmethod
    def users_list(user_id, team_id):
        token = des.decrypt(bytes(db_interface.search_slack_workspace(team_id)))
        token = token[0:-4].decode('utf-8')
        print("token here: ", token)  # tirar esse print
        client1 = SlackClient(token)

        channels = []
        members = []

        users_conv = client1.api_call(
            "users.conversations",
            user=user_id
        )
        print(users_conv)
        for channel in users_conv["channels"]:
            channels.append(channel["id"])

        # print("channels list: ", channels)

        for channel in channels:
            channel_info = client1.api_call("channels.info", channel=channel)
            for member in channel_info["channel"]["members"]:
                members.append(member)

        print("members list: ", members)

        return members
