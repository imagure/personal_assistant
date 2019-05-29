from dialog_manager.DialogManagerSelector import DialogManagerSelector as dms
from dialog_message.dialog_message import DialogMessage as dmessage

dmselector = dms()
dmselector.start()
# um compromisso e uma aceitacao
print('marcar compromisso')
dmsg = dmessage(['marcar_compromisso'], ['reunion'], [2],
                [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 7)
dmselector.dispatch_msg(dmsg, 'en')
input('digite algo ...')
print('confirmacao')
dmsg = dmessage(['confirmacao'], ['reunion'], [7],
                [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 2)
dmselector.dispatch_msg(dmsg, 'en')
input('Recolocar compromisso no DM')
dmsg = dmessage(['chama_comprimisso'], ['reunion'], [7],
                [], [], ['bar'], ['02-01-01'], ['19:00:00'], [], 2)
dmselector.dispatch_msg(dmsg, 'en')
print('cria novo encontro')
print('marcar compromisso')
dmsg = dmessage(['marcar_compromisso'], ['reunion'], [3],
                [], [], ['bar'], ['01-01-01'], ['18:00:00'], [], 1)
dmselector.dispatch_msg(dmsg, 'en')
input('espera_ai')
print('solicitar adicao de pessoa')
dmsg = dmessage(['add_pessoa'], ['reunion'], [6],
                [], [], ['bar'], ['01-01-01'], ['18:00:00'], [], 3)
dmselector.dispatch_msg(dmsg, 'en')
input('ola')
print('aceitar pessoa')
dmsg = dmessage(['confirmacao'], ['reunion'], [3],
                [], [], ['bar'], ['01-01-01'], ['18:00:00'], [], 1)
dmselector.dispatch_msg(dmsg, 'en')
input('ola')
print('aceitar compromisso')
dmsg = dmessage(['confirmacao'], ['reunion'], [3],
                [], [], ['bar'], ['01-01-01'], ['18:00:00'], [], 3)
dmselector.dispatch_msg(dmsg, 'en')
input('ola')
print('aceitar compromisso')
dmsg = dmessage(['confirmacao'], ['reunion'], [3],
                [], [], ['bar'], ['01-01-01'], ['18:00:00'], [], 6)
dmselector.dispatch_msg(dmsg, 'en')
