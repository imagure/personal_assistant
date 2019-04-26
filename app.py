import os

from flask import Flask
from flask_restful import Api, Resource, reqparse

from semanticizer.semanticizer_worker import SemanticizerWorker

app = Flask(__name__)
api = Api(app)


class PersonalAssistantPortuguese(Resource):

    semanticizer = SemanticizerWorker(language='pt')
    semanticizer.start()

    def get(self):
        return "Flask server up and running!", 200

    def post(self):
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
            return "No phrase was received", 404

        return "Estou analisando sua frase!  ;)", 200


class PersonalAssistantEnglish(Resource):

    semanticizer = SemanticizerWorker(language='en')
    semanticizer.start()

    def get(self):
        return "Flask server up and running!", 200

    def post(self):
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
            return "No phrase was received", 404

        return "I'm analyzing your phrase!  ;)", 200


api.add_resource(PersonalAssistantPortuguese, "/assistente_pessoal")
api.add_resource(PersonalAssistantEnglish, "/personal_assistant")

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)
