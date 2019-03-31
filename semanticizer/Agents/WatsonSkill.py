from __future__ import print_function
import re
from watson_developer_cloud import AssistantV1
from semanticizer import entity_class as ec
import json
from configs import *


class WatsonSkill:
    f = open("configs/watson_assistant.json")
    with open("configs/watson_assistant.json") as f:
        data = json.load(f)

    assistant = AssistantV1(
        username=data["WatsonAssistant"]["username"],
        password=data["WatsonAssistant"]["password"],
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        url=data["WatsonAssistant"]["url"],
        version=data["WatsonAssistant"]["version"])

    def __init__(self, language, mode, input_text):
        self.language = language
        if language == 'pt':
            if mode == 'regular':
                self.workspace_id = self.data["WatsonWorkspaces"]["regular_pt"]
            elif mode == 'response':
                self.workspace_id = self.data["WatsonWorkspaces"]["response_pt"]
        elif language == 'en':
            if mode == 'regular':
                self.workspace_id = self.data["WatsonWorkspaces"]["regular_en"]
            elif mode == 'response':
                self.workspace_id = self.data["WatsonWorkspaces"]["response_en"]
        self.response = None
        self.mode = mode
        self.input_text = input_text

    def get_workspace_id(self):
        return 'Workspace id {0}'.format(self.workspace_id)

    def get_response(self):
        input_text = re.sub('\s+', ' ', self.input_text)
        self.response = self.assistant.message(
            workspace_id=self.workspace_id,
            input={'text': input_text}).get_result()

    def get_intent(self):
        if self.response['intents'] != []:
            intent = self.response['intents'][0]['intent']
            print("\nO 'modo de uso' é: ", self.mode)
            print("A intenção detectada pelo Watson foi: ", intent)
            print("O nível de confiança foi: ", self.response['intents'][0]['confidence'])
            print("")
            if self.mode == 'response':
                intent = self.fallback_intent(intent)
        elif self.response['intents'] == [] and self.mode == 'response':
            print("\nNenhuma intenção de confirmação detectada!")
            intent = self.fallback_intent()
        else:
            intent = []

        return intent

    def fallback_intent(self, intent=None):
        if self.language == 'pt':
            self.workspace_id = self.data["WatsonWorkspaces"]["regular_pt"]
        elif self.language == 'en':
            self.workspace_id = self.data["WatsonWorkspaces"]["regular_en"]
        self.get_response()
        if self.response['intents'] != [] and intent is not None:
            if self.response['intents'][0]['confidence'] > 0.5:
                return self.response['intents'][0]['intent']
            else:
                return intent
        elif self.response['intents'] == [] and intent is not None:
            return intent
        else:
            return self.response['intents'][0]['intent']

    def get_date_time(self):
        date_entities = []
        hour_entities = []
        found_entities = []
        for item in self.response['entities']:
            if item['entity'] == 'sys-date':
                entities = self.format_answer(item, 'date')
                date_entities.append(entities[0])
                found_entities.append(entities[1])
            elif item['entity'] == 'sys-time':
                entities = self.format_answer(item, 'hour')
                hour_entities.append(entities[0])
                found_entities.append(entities[1])
        print("\nAs datas/tempo detectadas pelo Watson foram: ", found_entities)
        print("")
        return found_entities, date_entities, hour_entities

    def format_answer(self, item, datetime):
        location = item['location']
        text = self.input_text[location[0]:location[1]]
        entity = ec.Entity(text=text, start=location[0],
                            end=location[1], tag='NP', pos=datetime, type=datetime)
        found_datetime = ec.Entity(text=item['value'], start=location[0],
                            end=location[1], tag='NP', pos=datetime, type=datetime)
        print(datetime, " text is: ", text)
        return entity, found_datetime
