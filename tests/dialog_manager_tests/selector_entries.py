from dialog_message.dialog_message import DialogMessage as dmessage
import time


def marcar_compromissos(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2, 3, 4],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 4)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('marcar compromisso 2')
    dmsg = dmessage(['marcar_compromisso'], ['party'], [1, 3, 4],
                    [], [], ['bar'], ['2019-09-04'], ['20:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 4)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input("Pressiona alguma tecla para continuar.")
    # time.sleep(10)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


def add_pessoa(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('add_pessoa')
    dmsg = dmessage(['add_pessoa'], [], [3],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')


def excl_pessoa(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2, 3],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('excl_pessoa')
    dmsg = dmessage(['excl_pessoa'], [], [3],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(15)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


def remarcar_dia_hora(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(10)

    print('remarcar_compromisso positivo')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], [], ['2019-09-30'], ['20:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao 2')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('remarcar_compromisso negativo')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], [], ['2019-09-30'], ['19:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)
    dmsg = dmessage(['resposta_negativa'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')


def remarcar_dia(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(10)

    print('remarcar_compromisso')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], [], ['2019-09-30'], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')


def remarcar_hora(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(10)

    print('remarcar_compromisso')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], [], [], ['20:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_mo(dmselector):
    print('remarcar compromisso 1')
    dmsg = dmessage(['remarcar_compromisso'], [], [2],
                    [], [], ['office'], ['2019-09-28'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [],
                    [], [], [], ['2019-09-30'], ['20:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_dia_mo(dmselector):
    print('remarcar compromisso 1')
    dmsg = dmessage(['remarcar_compromisso'], [], [2],
                    [], [], ['office'], ['2019-09-28'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [],
                    [], [], [], ['2019-09-30'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_hora_mo(dmselector):
    print('remarcar compromisso 1')
    dmsg = dmessage(['remarcar_compromisso'], [], [2],
                    [], [], ['office'], ['2019-09-28'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [],
                    [], [], [], [], ['20:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_add_pessoa_mo(dmselector):
    print('add_pessoa 1')
    dmsg = dmessage(['add_pessoa'], [], [2],
                    [], [], ['office'], ['2019-09-28'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [3],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_excl_pessoa_mo(dmselector):
    print('excl_pessoa 1')
    dmsg = dmessage(['excl_pessoa'], [], [2],
                    [], [], ['office'], ['2019-09-28'], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [2],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    #dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_not_mo(dmselector):
    print('remarcar compromisso 1')
    dmsg = dmessage(['remarcar_compromisso'], [], [1],
                    [], [], ['office'], ['2019-09-28'], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [],
                    [], [], [], ['2019-09-30'], ['20:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_add_pessoa_not_mo(dmselector):
    print('add_pessoa 1')
    dmsg = dmessage(['add_pessoa'], [], [1],
                    [], [], ['office'], ['2019-09-28'], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [3],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')


def reviver_compromisso_excl_pessoa_not_mo(dmselector):
    print('add_pessoa 1')
    dmsg = dmessage(['excl_pessoa'], [], [1],
                    [], [], ['office'], ['2019-09-28'], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('mandar informação')
    dmsg = dmessage([], [], [3],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(5)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')
