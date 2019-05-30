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
    dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                    [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['meeting'], [7],
                    [], [], ['restaurant'], ['04-04-04'], ['09:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['party'], [7],
                    [], [], ['saloon'], ['05-05-05'], ['23:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('marcar compromisso')
    dmsg = dmessage(['marcar_compromisso'], ['work'], [1, 7],
                    [], [], ['office'], ['03-03-03'], ['14:00:00'], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('confirmacao')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 7)
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
                    [], [], [], [], [], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso sem ser MO')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['office'], ['02-01-01'], ['17:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Responde com info a ser alterada')
    dmsg = dmessage([], [], [],
                    [], [], [], ['02-01-01'], ['16:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('MO confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso sendo MO')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['bar'], ['03-03-03'], ['12:00:00'], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Confirma informação sendo MO')
    dmsg = dmessage([], [], [],
                    [], [], [], ['02-01-01'], ['20:00:00'], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

elif mode == "r3":

    input('PAUSE! digite algo para continuar...')

    print('Remarcar compromisso sem ser MO')
    dmsg = dmessage(['remarcar_compromisso'], [], [],
                    [], [], ['office'], ['02-01-01'], ['17:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('Responde com info a ser alterada')
    dmsg = dmessage([], [], [],
                    [], [], [], ['02-01-01'], ['16:00:00'], [], 1)
    dmselector.dispatch_msg(dmsg, 'en')

    input('PAUSE! digite algo para continuar...')

    print('MO confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 2)
    dmselector.dispatch_msg(dmsg, 'en')

    print('MO confirma')
    dmsg = dmessage(['confirmacao'], [], [],
                    [], [], [], [], [], [], 7)
    dmselector.dispatch_msg(dmsg, 'en')

dmselector.join()
