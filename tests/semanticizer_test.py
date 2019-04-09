from semanticizer.Semanticizer import Semanticizer as semanticizer
from dialog_message.dialog_message import *
import pytest
import json


@pytest.fixture
def msgs():
    with open("tests/tests_data/semanticizer_io.json") as f:
        data = json.load(f)
    return data["test_msg"], data["test_ans"]


def test_semanticizer(msgs):
    i = 0
    while i < len(msgs[0]):
        my_json = semanticizer('response', 'en').semantize(msgs[0][i])
        message = DialogMessage.from_json(my_json)
        assert message.intent == msgs[1][i]["intent"], 'Should be {}'.format(msgs[1][i]["intent"])
        assert message.commitment == msgs[1][i]["commitment"], 'Should be {}'.format(msgs[1][i]["commitment"])
        assert message.person_know == msgs[1][i]["person_known"], 'Should be {}'.format(msgs[1][i]["person_known"])
        assert message.person_unknown == msgs[1][i]["person_unknown"], 'Should be {}'.format(msgs[1][i]["person_unknown"])
        assert message.place_known == msgs[1][i]["place_known"], 'Should be {}'.format(msgs[1][i]["place_known"])
        assert message.place_unknown == msgs[1][i]["place_unknown"], 'Should be {}'.format(msgs[1][i]["place_unknown"])
        assert message.date == msgs[1][i]["date"], 'Should be {}'.format(msgs[1][i]["date"])
        assert message.hour == msgs[1][i]["hour"], 'Should be {}'.format(msgs[1][i]["hour"])
        i += 1


def main():
    test_semanticizer(msgs)


if __name__ == '__main__':
    main()
