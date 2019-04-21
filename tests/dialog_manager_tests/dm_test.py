from dialog_manager.dialog_manager import DialogManager
import pytest
import json

dm = DialogManager()
dm.start()
dm.og.set_language('pt')

with open("tests/tests_examples/dialog_manager_io.json") as f:
    data = json.load(f)

messages = []
i = 0
while i < len(data["test_msg"]):
    message = data["test_msg"][i]
    dm.dispatch_msg(message)
    i += 1
    #retirar resultado de algum lugar


@pytest.fixture
def msgs():
    return messages, data["test_ans"]


def test_dm(msgs):
    i = 0
    while i < len(data["test_msg"]):
        assert msgs[0] == msgs[1]
        i += 1


def main():
    test_dm(msgs)


if __name__ == '__main__':
    main()
