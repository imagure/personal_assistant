from slackclient import SlackClient

slack_token = "xoxp-594442784566-594078665495-594140143367-1ab73b6dc2af6708e8491518ff515091"
sc = SlackClient(slack_token)


class SlackHelper(object):

    def post_msg(self, response, channel_id):
        sc.api_call(
            "chat.postMessage",
            username="Personal Assistant",
            channel=channel_id,
            text=response,
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
