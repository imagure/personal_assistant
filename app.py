from flask import Flask
from flask_restful import Api, Resource, reqparse
import io_manager as io
import os

app = Flask(__name__)
api = Api(app)


class PersonalAssistant(Resource):

    io = io.IOManager(language='pt')
    io.start()

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
        args = parser.parse_args()
        text = args["text"]
        channel_id = args["channel_id"]
        response_url = args["response_url"]

        if text is not None and response_url is not None \
                and channel_id is not None:
            self.io.dispatch_channel(channel_id)
            self.io.dispatch_msg(text)

        else:
            return "No phrase was received", 404

        return 'Sua frase stá sendo analisada!  ;)', 200


class PersonalAssistantEnglish(Resource):

    io = io.IOManager(language='en')
    io.start()

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
        args = parser.parse_args()
        text = args["text"]
        channel_id = args["channel_id"]
        response_url = args["response_url"]

        if text is not None and response_url is not None \
                and channel_id is not None:
            self.io.dispatch_channel(channel_id)
            self.io.dispatch_msg(text)

        else:
            return "No phrase was received", 404

        return 'Your phrase is being analyzed!  ;)', 200


api.add_resource(PersonalAssistant, "/assistente_pessoal")
api.add_resource(PersonalAssistantEnglish, "/personal_assistant")

port = int(os.environ.get('PORT', 5000))

app.run(debug=True, host='0.0.0.0', port=port)
