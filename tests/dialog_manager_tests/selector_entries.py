from dialog_message.dialog_message import DialogMessage as dmessage
import time


def marcar_compromissos(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2, 3],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('marcar compromisso 2')
    dmsg = dmessage(['marcar_compromisso'], ['party'], [1, 3],
                    [], [], ['bar'], ['2019-09-04'], ['20:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('marcar compromisso 3')
    dmsg = dmessage(['marcar_compromisso'], ['meeting'], [1, 2],
                    [], [], ['cinema'], ['2019-11-22'], ['18:00:00'], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(3)

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
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


def remarcar_compromisso(dmselector):
    print('marcar compromisso 1')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['office'], ['2019-09-28'], ['18:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    time.sleep(10)

    print('remarcar_compromisso')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
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

