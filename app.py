import os

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from slackclient import SlackClient
from semanticizer.SemanticizerWorker import SemanticizerWorker

client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]
oauth_scope = os.environ["scope"]

# client_id = "594442784566.594081769079"
# client_secret = "b1c6ea964deecdf37068ce2bf6cb1977"
# oauth_scope = "bot,commands,chat:write:bot,channels:write,groups:write,mpim:write,im:write,channels:read,groups:read,mpim:read,im:read"

app = Flask(__name__)
api = Api(app)

slack_team_tokens = {}


class PersonalAssistant(Resource):

    semanticizer = SemanticizerWorker()
    semanticizer.start()

    def get(self):
        rule = request.url_rule
        if "begin_auth" in rule.rule:
            return self.pre_install()
        elif "finish_auth" in rule.rule:
            return self.post_install()
        return "Flask server up and running!", 200

    @staticmethod
    def pre_install():
        return '''
          <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
              Add to Slack
          </a>
      '''.format(oauth_scope, client_id)

    @staticmethod
    def post_install():

        # Retrieve the auth code from the request params
        auth_code = request.args['code']
        print("Auth_code: ", auth_code)

        # An empty string is a valid token for this request
        sc = SlackClient("")

        # Request the auth tokens from Slack
        auth_response = sc.api_call(
            "oauth.access",
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )

        os.environ[auth_response["team_id"]] = auth_response['access_token']

        slack_user_token = auth_response['access_token']
        slack_bot_token = auth_response['bot']['bot_access_token']

        print("slack user token: ", slack_user_token)
        print("slack bot: ", slack_bot_token)

        slack_team_tokens[auth_response["team_id"]] = auth_response['access_token']

        # Don't forget to let the user know that auth has succeeded!
        return "Auth complete!"

    def post(self):

        rule = request.url_rule
        if "finish_auth" in rule.rule:
            print("Entrei no finish")
            return self.post_install()

        else:
            self._set_semanticizer_language()

            parser = reqparse.RequestParser()
            parser.add_argument("text")
            parser.add_argument("channel_id")
            parser.add_argument("response_url")
            parser.add_argument("user_name")
            parser.add_argument("user_id")
            parser.add_argument("team_id")
            args = parser.parse_args()

            text = args["text"]
            channel_id = args["channel_id"]
            response_url = args["response_url"]
            user_name = args["user_name"]
            user_id = args["user_id"]
            team_id = args["team_id"]

            if text is not None and response_url is not None \
                    and channel_id is not None:
                self.semanticizer.dispatch_msg(text, channel_id,
                                               user_name, user_id, team_id)
            else:
                return self._error_return_msg(), 404

            return self._success_return_msg(text), 200

    def _set_semanticizer_language(self):

        rule = request.url_rule
        if "assistente_pessoal" in rule.rule:
            self.semanticizer.set_language("pt")
        elif "personal_assistant" in rule.rule:
            self.semanticizer.set_language("en")

    @staticmethod
    def _error_return_msg():

        rule = request.url_rule
        if "assistente_pessoal" in rule.rule:
            return "Não conseguimos receber sua mensagem. Tente novamente em breve."
        return "We couldn't receive your message. Try again soon."

    @staticmethod
    def _success_return_msg(text):

        rule = request.url_rule
        if "assistente_pessoal" in rule.rule:
            return "Estou analisando sua frase: '{}'.".format(text)
        return "I'm analyzing your phrase: '{}'.".format(text)


api.add_resource(PersonalAssistant, "/assistente_pessoal", "/personal_assistant", "/begin_auth", "/finish_auth")
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)
