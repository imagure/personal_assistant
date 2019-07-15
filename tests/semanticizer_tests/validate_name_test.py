from semanticizer.Semanticizer import Semanticizer as semanticizer
from semanticizer.Agents.initializer import Initializer
import json


initial_vars = Initializer()
initial_vars.set_spacy_models()

test_semanticizer = semanticizer('response', initial_vars, user_id=1)
language = "en"

with open("tests/tests_examples/names.json") as f:
    data = json.load(f)

test_names = data["test_names"]
test_phrases = data["test_phrases"]
test_wrong_phrases = data["test_wrong_phrases"]


def test_find_solo_name():
    i = 0
    while i < len(test_names):
        found_name = test_semanticizer.find_name_only(test_names[i])
        assert found_name == test_names[i], \
            'Should be {}'.format(test_names[i])
        i += 1


def test_find_phrase_name():
    i = 0
    while i < len(test_names):
        found_name = test_semanticizer.find_name_only(test_phrases[i])
        assert found_name == test_names[i], \
            'Should be {}'.format(test_names[i])
        i += 1


def test_wrong_names():
    i = 0
    while i < len(test_wrong_phrases):
        found_name = test_semanticizer.find_name_only(test_wrong_phrases[i])
        assert found_name == '', \
            'Should be {}'.format('')
        i += 1

