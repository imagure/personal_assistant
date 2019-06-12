import os

from slackclient import SlackClient

slack_user_token = {"THGD0P2GN": "xoxp-594442784566-594078665495-593343524389-fecda7db64b17348c9ac1aa83970284b",
                    "TKE8JAR1N": "xoxp-660290365056-663620194022-661521259269-0e7fbc95d9830c8a077706136e9cafb1"}

test_client = SlackClient(slack_user_token["THGD0P2GN"])


class SlackHelper(object):

    @staticmethod
    def post_msg(response, channel_id, team_id=None):
        print("token here: ", os.environ[team_id])
        client1 = SlackClient(slack_user_token[team_id])
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
        print("token here: ", os.environ[team_id])
        client1 = SlackClient(slack_user_token[team_id])
        user_channel = client1.api_call("conversations.open", users=user_id)
        print(user_channel)
        return user_channel["channel"]["id"]

    @staticmethod
    def users_list(user_id, team_id):
        print("token here: ", os.environ[team_id])
        client1 = SlackClient(slack_user_token[team_id])

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
