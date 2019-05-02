from __future__ import print_function

import json
import os
import re

from ibm_watson import AssistantV1

from semanticizer import entity_class as ec


class WatsonSkill(object):

    with open("configs/watson_assistant.json") as f:
        data = json.load(f)

    assistant = AssistantV1(
        username=data["WatsonAssistant"]["username"],
        password=data["WatsonAssistant"]["password"],
        url=data["WatsonAssistant"]["url"],
        version=data["WatsonAssistant"]["version"])

    workspace_id = None
    response = None

    def __init__(self, language, mode, input_text):
        self.language = language
        self.set_workspace(mode)
        self.mode = mode
        self.input_text = input_text

    def set_workspace(self, mode):
        if self.language == 'pt':
            if mode == 'regular':
                self.workspace_id = self.data["WatsonWorkspaces"]["regular_pt"]
            elif mode == 'response':
                self.workspace_id = self.data["WatsonWorkspaces"]["response_pt"]
        elif self.language == 'en':
            if mode == 'regular':
                self.workspace_id = self.data["WatsonWorkspaces"]["regular_en"]
            elif mode == 'response':
                self.workspace_id = self.data["WatsonWorkspaces"]["response_en"]

    def get_workspace_id(self):
        return 'Workspace id {0}'.format(self.workspace_id)

    def get_response(self):
        input_text = re.sub('\s+', ' ', self.input_text)
        response = self.assistant.message(
            workspace_id=self.workspace_id,
            input={'text': input_text}).get_result()
        if response is not None:
            self.response = response
        else:
            self.response['intents'] = []
            self.response['entities'] = []

    def get_intent(self):
        print("-" * 20, "> WatsonSkill")
        if self.response['intents'] != []:
            intent = self.response['intents'][0]['intent']
            confidence = self.response['intents'][0]['confidence']
            if self.mode == 'response':
                intent, confidence = self.fallback_intent(intent, confidence)
        elif self.response['intents'] == [] and self.mode == 'response':
            print("Nenhuma intenção de confirmação detectada!")
            intent, confidence = self.fallback_intent()
        else:
            intent = ""
            confidence = 0

        print("O 'modo de uso' é: ", self.mode)
        print("A intenção detectada pelo Watson foi: ", intent)
        print("O nível de confiança foi: ", confidence)

        return intent

    def fallback_intent(self, intent=None, confidence=None):
        if self.language == 'pt':
            self.workspace_id = self.data["WatsonWorkspaces"]["regular_pt"]
        elif self.language == 'en':
            self.workspace_id = self.data["WatsonWorkspaces"]["regular_en"]
        self.get_response()
        if self.response['intents'] and intent is not None:
            if self.response['intents'][0]['confidence'] > 0.5:
                return self.response['intents'][0]['intent'], self.response['intents'][0]['confidence']
            else:
                return intent, confidence
        elif self.response['intents'] and intent is None:
            return self.response['intents'][0]['intent'], self.response['intents'][0]['confidence']
        elif not self.response['intents']:
            return intent, confidence

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
        return found_entities, date_entities, hour_entities

    def format_answer(self, item, datetime):
        location = item['location']
        text = self.input_text[location[0]:location[1]]
        entity = ec.Entity(text=text, start=location[0],
                            end=location[1], tag='NP', pos=datetime, type=datetime)
        found_datetime = ec.Entity(text=item['value'],
                            tag='NP', pos=datetime, type=datetime)
        print(datetime, " text is: ", text)
        return entity, found_datetime
