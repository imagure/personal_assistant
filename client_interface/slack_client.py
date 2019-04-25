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

    def users_list(self, ):
        users_list = sc.api_call(
            "users.list",
        )

        for user in users_list["members"]:
            user_name = user["real_name"]
            user_id = user["id"]
            team_id = user["team_id"]
            # search db for users
