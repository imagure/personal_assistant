from slackclient import SlackClient

slack_token = "xoxp-594442784566-594078665495-594140143367-1ab73b6dc2af6708e8491518ff515091"
sc = SlackClient(slack_token)


class SlackHelper(object):

    def post_msg(self, response, channel_id):
        sc.api_call(
            "chat.postMessage",
            username="PersonalAssistant",
            channel=channel_id,
            as_user=False,
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/"
                     "Mr._Smiley_Face.svg/2000px-Mr._Smiley_Face.svg.png",
            text=response
        )

    def users_list(self, user_id):
        channels = []
        members = []

        users_conv = sc.api_call(
            "users.conversations",
            user=user_id
        )

        for channel in users_conv["channels"]:
            channels.append(channel["id"])

        # print("channels list: ", channels)

        for channel in channels:
            channel_info = sc.api_call("channels.info", channel=channel)
            for member in channel_info["channel"]["members"]:
                members.append(member)

        # print("members list: ", members)

        # for member in members:
            # query for members in the DB here

        # return the names of the users found on the DB
