from db.sql.create_db_model import *
from db.sql.db_interface import DbInterface
from db.sql.popula_dbTest import *
from dialog_manager.DialogManagerSelector import DialogManagerSelector as dms
from output_generator.OutputGenerator import OutputGenerator
from tests.dialog_manager_tests.popula_encontros_teste import *
from tests.dialog_manager_tests.selector_entries import *

db_interface = DbInterface()

og = OutputGenerator()

dmselector = dms(og=og)


def create_tables():
    create_model('local')


def popula_db_teste():
    populate_usuario()


def popula_encontros_diretamente():
    populate_encontro()
    populate_listaencontro_1()


def test_marcar_compromisso():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    marcar_compromissos(dmselector)

    dmselector.join()
    og.join()


def test_adicionar_pessoa():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    add_pessoa(dmselector)

    dmselector.join()
    og.join()


def test_excl_pessoa():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    excl_pessoa(dmselector)

    dmselector.join()
    og.join()


def test_remarcar_dia_hora():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    remarcar_dia_hora(dmselector)

    dmselector.join()
    og.join()


def test_remarcar_dia():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    remarcar_dia(dmselector)

    dmselector.join()
    og.join()


def test_remarcar_hora():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()

    remarcar_hora(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_dia_hora_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_dia_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_dia_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_hora_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_hora_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_add_pessoa_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    populate_encontro()
    populate_listaencontro_2()

    reviver_compromisso_add_pessoa_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_excl_pessoa_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_excl_pessoa_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_not_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_not_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_add_pessoa_not_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    populate_encontro()
    populate_listaencontro_2()

    reviver_compromisso_add_pessoa_not_mo(dmselector)

    dmselector.join()
    og.join()


def test_reviver_encontro_excl_pessoa_not_mo():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    popula_encontros_diretamente()

    reviver_compromisso_excl_pessoa_not_mo(dmselector)

    dmselector.join()
    og.join()


if __name__ == "__main__":
    print("Testes: ")
    print(" 1: marcar múltiplos compromissos ao mesmo tempo (Não funciona com sobreposição de encontros)")
    print("")
    print(" 2: sugerir adicionar pessoa (antes de confirmar)")
    print(" 3: sugerir excluir pessoa (antes de confirmar) (Não está excluindo do DB)")
    print(" 4: sugerir remarcar dia e hora (antes de confirmar)")
    print(" 5: sugerir remarcar dia (antes de confirmar)")
    print(" 6: sugerir remarcar hora (antes de confirmar)")
    print("")
    print(" 7: reviver encontro e remarcar dia e hora sendo o MO (Corrigir: está mudando apenas a hora)")
    print(" 8: reviver encontro e remarcar dia sendo o MO")
    print(" 9: reviver encontro e remarcar hora sendo o MO")
    print(" 10: reviver encontro e adicionar pessoa sendo o MO")
    print(" 11: reviver encontro e excluir pessoa sendo o MO")
    print("")
    print(" 12: reviver encontro e remarcar dia e hora sem ser MO (Mudança de dia e hora funcionando!)")
    print(" 13: reviver encontro e adicionar pessoa sem ser MO")
    print(" 14: reviver encontro e excluir pessoa sem ser MO")

    teste = int(input("Qual teste deseja rodar?  > "))

    if teste == 1:
        test_marcar_compromisso()
    elif teste == 2:
        test_adicionar_pessoa()
    elif teste == 3:
        test_excl_pessoa()
    elif teste == 4:
        test_remarcar_dia_hora()
    elif teste == 5:
        test_remarcar_dia()
    elif teste == 6:
        test_remarcar_hora()
    elif teste == 7:
        test_reviver_encontro_dia_hora_mo()
    elif teste == 8:
        test_reviver_encontro_dia_mo()
    elif teste == 9:
        test_reviver_encontro_hora_mo()
    elif teste == 10:
        test_reviver_encontro_add_pessoa_mo()
    elif teste == 11:
        test_reviver_encontro_excl_pessoa_mo()
    elif teste == 12:
        test_reviver_encontro_not_mo()
    elif teste == 13:
        test_reviver_encontro_add_pessoa_not_mo()
    elif teste == 14:
        test_reviver_encontro_excl_pessoa_not_mo()
