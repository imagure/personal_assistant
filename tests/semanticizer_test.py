from semanticizer.Semanticizer import Semanticizer as semanticizer

test_msg = "I want to schedule a meeting tonight with Ricardo at the bar"
test_ans = {
    "intent": ["marcar_compromisso"],
    "commitment": ["meeting"],
    "person_known": [["Ricardo tatsuya", "Ricardo Imagure"]],
    "person_unknown": [],
    "place_known": [],
    "place_unknown": ["bar"],
    "date": ["2019-04-08"],
    "hour": ["18:00:00"],
    "dont_know": []
  }


def test_semanticizer():
    assert semanticizer('response', 'en').semantize(test_msg) == test_ans, "Should be {}".format(test_ans)


test_semanticizer()
