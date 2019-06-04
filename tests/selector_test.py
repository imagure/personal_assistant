from dialog_manager.DialogManagerSelector import DialogManagerSelector as dms
from dialog_message.dialog_message import DialogMessage as dmessage
from output_generator.OutputGenerator import OutputGenerator

og = OutputGenerator()
og.start()

dmselector = dms(og=og)
dmselector.start()
mode = input('Mode switch: ')

if mode == "i":

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [5],
                    [], [], ['bar'], ['02-01-01'], ['18:00:00'], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 5)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [5],
                    [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 5)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['meeting'], [3],
                    [], [], ['restaurant'], ['04-04-04'], ['09:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['party'], [3],
                    [], [], ['saloon'], ['05-05-05'], ['23:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['work'], [1, 3],
                    [], [], ['office'], ['03-03-03'], ['14:00:00'], [], 5)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


elif mode == "r":

    input('PAUSE! digite algo para continuar...')

    print('Remarcar_compromisso sem info')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso mo')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['bar'], [], [], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso not mo')
    dmsg = dmessage(['remarcar_compromisso'], ['reunion'], [7],
                    [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

elif mode == "r2":

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso sem info')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['bar'], [], [], [], 3)
    dmselector.dispatch_msg(dmsg, 'en')


elif mode == "r3":

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso sem ser MO')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['office'], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Responde com info a ser alterada')
    dmsg = dmessage([], [], [],
                    [], [], [], ['02-01-01'], ['17:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('MO confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 5)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('01 confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('03 confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

dmselector.join()
