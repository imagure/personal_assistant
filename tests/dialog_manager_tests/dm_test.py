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
    populate('local')


def popula_encontros_diretamente():
    populate_encontro()
    populate_listaencontro()


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


def test_remarcar_encontro():
    dmselector.start()
    og.start()
    create_tables()
    popula_db_teste()
    remarcar_compromisso(dmselector)
    dmselector.join()
    og.join()


if __name__ == "__main__":
    # test_adicionar_pessoa()
    test_remarcar_encontro()
