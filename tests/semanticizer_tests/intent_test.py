from semanticizer.Semanticizer import Semanticizer as semanticizer
from dialog_message.dialog_message import *
import pytest
import json


@pytest.fixture
def msgs():
    with open("tests/tests_examples/semanticizer_io.json") as f:
        data = json.load(f)
    return data["test_msg"], data["test_ans"]


def test_intent(msgs):
    i = 0
    while i < len(msgs[0]):
        my_json = semanticizer('response', 'en').semantize(msgs[0][i])
        message = DialogMessage.from_json(my_json)
        assert message.intent == msgs[1][i]["intent"], 'Should be {}'.format(msgs[1][i]["intent"])
        i += 1


def main():
    test_intent(msgs)


if __name__ == '__main__':
    main()
