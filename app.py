import os

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from semanticizer.SemanticizerWorker import SemanticizerWorker

app = Flask(__name__)
api = Api(app)


class PersonalAssistant(Resource):

    semanticizer = SemanticizerWorker()
    semanticizer.start()

    @staticmethod
    def get():

        return "Flask server up and running!", 200

    def post(self):

        self._set_semanticizer_language()

        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("channel_id")
        parser.add_argument("response_url")
        parser.add_argument("user_name")
        parser.add_argument("user_id")
        args = parser.parse_args()

        text = args["text"]
        channel_id = args["channel_id"]
        response_url = args["response_url"]
        user_name = args["user_name"]
        user_id = args["user_id"]

        if text is not None and response_url is not None \
                and channel_id is not None:
            self.semanticizer.dispatch_msg(text, channel_id,
                                           user_name, user_id)
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


api.add_resource(PersonalAssistant, "/assistente_pessoal", "/personal_assistant")
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)
