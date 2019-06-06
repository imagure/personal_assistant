from semanticizer.Semanticizer import Semanticizer as semanticizer
from semanticizer.Agents.initializer import Initializer

initial_vars = Initializer()
initial_vars.set_spacy_models()

test_semanticizer = semanticizer('response', initial_vars, user_id=1)
language = "en"

names_list_en = open("tests/tests_examples/names_en.txt")
names_list_pt = open("tests/tests_examples/names_pt.txt")


def test_find_solo_name_from_list_en():
    errors = 0
    size = 0
    for name in names_list_en:
        size += 1
        found_name = test_semanticizer.find_name_only(name)
        if name.strip("\n") != found_name:
            print("[Erro] -> ", name)
            errors += 1
    return errors/size


def test_find_solo_name_from_list_pt():
    errors = 0
    size = 0
    for name_surname in names_list_pt:
        name = name_surname.split()[0]
        size += 1
        found_name = test_semanticizer.find_name_only(name)
        if name.strip("\n") != found_name:
            print("[Erro] -> ", name)
            errors += 1
    return errors/size


if __name__=="__main__":
    taxa_pt = test_find_solo_name_from_list_pt()
    taxa_en = test_find_solo_name_from_list_en()
    print("[Resultados]")
    print("Taxa de erros em PT: ", taxa_pt)
    print("Taxa de erros em EN: ", taxa_en)
