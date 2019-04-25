import os

from flask import Flask
from flask_restful import Api, Resource, reqparse

from semanticizer.semanticizer_worker import SemanticizerWorker

app = Flask(__name__)
api = Api(app)


class PersonalAssistant(Resource):

    semanticizer = SemanticizerWorker(language='pt')
    semanticizer.start()

    responses = []

    def __init__(self):
        pass

    def get(self):
        return self.responses, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("channel_id")
        parser.add_argument("response_url")
        parser.add_argument("user_name")
        args = parser.parse_args()
        text = args["text"]
        channel_id = args["channel_id"]
        response_url = args["response_url"]
        user_name = args["user_name"]

        if text is not None and response_url is not None \
                and channel_id is not None:
            self.semanticizer.dispatch_msg(text, channel_id, user_name)

        else:
            return "No phrase was received", 404

        return 'Estamos analisando sua frase!  ;)', 200


class PersonalAssistantEnglish(Resource):

    semanticizer = SemanticizerWorker(language='en')
    semanticizer.start()

    responses = []

    def __init__(self):
        pass

    def get(self):
        return self.responses, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("channel_id")
        parser.add_argument("response_url")
        parser.add_argument("user_name")
        args = parser.parse_args()
        text = args["text"]
        channel_id = args["channel_id"]
        response_url = args["response_url"]
        user_name = args["user_name"]

        if text is not None and response_url is not None \
                and channel_id is not None:
            self.semanticizer.dispatch_msg(text, channel_id, user_name)

        else:
            return "No phrase was received", 404

        return 'Your phrase is being analyzed!  ;)', 200


api.add_resource(PersonalAssistant, "/assistente_pessoal")
api.add_resource(PersonalAssistantEnglish, "/personal_assistant")

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)
