from semanticizer.Semanticizer import Semanticizer as semanticizer
from dialog_message.dialog_message import *
import pytest
import json
from semanticizer.Agents.initializer import Initializer

sm_ontology = "db/Ontology/assistant.owl"
initial_vars = Initializer()
initial_vars.set_synsets()
initial_vars.set_ontology(sm_ontology)
initial_vars.set_spacy_models()

with open("tests/tests_examples/semanticizer_io_en.json") as f:
    data = json.load(f)
    
messages = []
i = 0
while i < len(data["test_msg"]):
    my_json = semanticizer('response', data["language"], initial_vars, user_id=1).semantize(data["test_msg"][i])
    messages.append(DialogMessage.from_json(my_json))
    i += 1


@pytest.fixture
def msgs():
    return messages, data["test_ans"]


def test_intent(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].intent == msgs[1][i]["intent"]["value"], \
            'Should be {}'.format(msgs[1][i]["intent"])
        i += 1


def test_commitment(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].commitment == msgs[1][i]["commitment"]["value"], \
            'Should be {}'.format(msgs[1][i]["commitment"])
        i += 1


def test_person_known(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].person_know == msgs[1][i]["person_known"]["value"], \
            'Should be {}'.format(msgs[1][i]["person_known"])
        i += 1


def test_person_unknown(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].person_unknown == msgs[1][i]["person_unknown"]["value"], \
            'Should be {}'.format(msgs[1][i]["person_unknown"])
        i += 1


def test_place_known(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].place_known == msgs[1][i]["place_known"]["value"], \
            'Should be {}'.format(msgs[1][i]["place_known"])
        i += 1


def test_place_unknown(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].place_unknown == msgs[1][i]["place_unknown"]["value"], \
            'Should be {}'.format(msgs[1][i]["place_unknown"])
        i += 1


def test_date(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].date == msgs[1][i]["date"]["value"], \
            'Should be {}'.format(msgs[1][i]["date"])
        i += 1


def test_hour(msgs):
    i = 0
    while i < len(msgs[0]):
        assert msgs[0][i].hour == msgs[1][i]["hour"]["value"], \
            'Should be {}'.format(msgs[1][i]["hour"])
        i += 1
