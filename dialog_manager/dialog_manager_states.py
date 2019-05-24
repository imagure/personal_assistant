from dialog_manager.State import *
from dialog_manager.initial_info_fsm import initial_info_fsm
from dialog_message import dialog_message
import json
import psycopg2
import queue


# from dialog_manager import DialogManager
# start of our FSM


class Idle(State):
    def __init__(self, income_data, dm):
        self.hasInternalEvent = False
        self.dm = dm
        #self.dm.db.set_state('Idle')
        self.income_data = income_data
        self.__name__ = 'Idle'

    def on_event(self, event):
        # any msg received from the semantizer will make the FSM go to InitialInfo
        if "marcar_compromisso" in event:
            print("[DialogManagerStates] Marcar compromisso disparado")
            if self.income_data.id_user:
                #retirado. passado para a criação do dm
                # postgres_insert_query = """ INSERT INTO Encontro (IDMEETINGOWNER) VALUES (%d) RETURNING ID """ % self.income_data.id_user
                cursor = self.dm.con.cursor()
                # cursor.execute(postgres_insert_query)
                # self.dm.con.commit()
                # self.dm.id_meeting = cursor.fetchone()[0]
                # self.dm.id_meeting_owner = self.income_data.id_user

                # adiciona meeting owner na withlist
                # select_query = """SELECT NOME from USUARIO WHERE ID = (%s)"""
                # cursor.execute(select_query, (self.dm.id_meeting_owner, ))
                # nome = cursor.fetchone()[0]
                self.dm.with_list.append(self.dm.id_meeting_owner)
                self.dm.con.commit()

                print("[DialogManagerStates] id_criado para o compromisso %d" %self.dm.id_meeting)
                # considera que o meeting owner sempre aceita o encontro
                postgres_insert_query = """INSERT INTO ListaEncontro (IDENCONTRO, IDCLIENTE, ACEITOU)
                                           VALUES(%s, %s, %s)"""
                # adiciona meeting owner a lista de eventos
                cursor.execute(postgres_insert_query, (self.dm.id_meeting, self.income_data.id_user, 1))
                self.dm.con.commit()
                return InitialInfo(self.dm)
            else:
                print("[DialogManagerStates] Usuario não identificado. Id ausente")
                return self
        elif "add_pessoa" in event:
            print("[DialogManagerStates]TODO: Tratamento para localizar encontro")
        return self


class InitialInfo(State):
    def __init__(self,  dm):
        self.hasInternalEvent = True
        self.ISM = initial_info_fsm.InitialInfoSM(dm)
        self.dm = dm
        self.__name__ = 'InitialInfo'
        # self.dm.db.set_state('InitialInfo')

    def on_event(self, event):
        if event == "info_finished":
            print('info_completed')
            return InfoCompleted(self.dm) # temporariamente retirado
            # Lembrar de tirar isso depois
            print("[DialogManagerStates] RESETANDO PARA IDLE! TIRAR DEPOIS!!")
            self.dm.with_list = []
            self.dm.where = []
            #when trocado por hour para consistencia
            self.dm.hour = []
            self.dm.date = []
            self.dm.commitment = []
            self.income_data = []

            return Idle('', self.dm)
        self.ISM.on_event(event)
        return self


class InfoCompleted(State):
    def __init__(self, dm):
        self.hasInternalEvent = True
        print("[DialogManagerStates] initial info completado")
        self.dm = dm
        self.__name__ = 'InfoCompleted'
        # self.dm.db.set_state('InfoCompleted')

    def on_event(self, event):
        self.income_data = self.dm.income_data
        if "remarcar_compromisso" in event:
            if self.income_data.hour != []:
                event = ['change_hour']
                self.income_data.intent = ['change_hour']
            elif self.income_data.date != []:
                event = ['change_date']
                self.income_data.intent = event
        if "mudar_lugar" in event or 'mudar_lugar_internal' in event or 'change_place' in event:  # intent event
            if self.dm.request_state is None and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeWhere(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage('change_place', [''], '', '', self.income_data.place_known,
                                                       self.income_data.place_unknown, '', '',
                                                       [self.income_data.id_user], self.dm.id_meeting_owner)
                # msg = json.dumps(message.__dict__)
                self.dm.output_queue.put(message)
                self.dm.send_output()
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeWhere(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

            # return ChangeWhere(self.dm)
        if "change_date" in event:
            if self.dm.request_state is None and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeDate(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage('change_date', [''], '',
                                                       '', '', '', self.income_data.date, '',
                                                       [self.income_data.id_user], self.dm.id_meeting_owner)
                # msg = json.dumps(message.__dict__)
                self.dm.output_queue.put(message)
                self.dm.send_output()
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeDate(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "change_hour" in event:
            if self.dm.request_state is None and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeHour(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage('change_hour', [''], '',
                                                       '', '', '', '', self.dm.income_data.hour,
                                                       [self.dm.income_data.id_user], self.dm.id_meeting_owner)
                # msg = json.dumps(message.__dict__)
                self.dm.output_queue.put(message)
                self.send_output()
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeHour(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "excl_pessoa" in event or "add_pessoa" in event:
            if self.dm.request_state is None and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeWithList(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage(event[0], [''], self.dm.income_data.person_know,
                                                       self.dm.income_data.person_unknown, '', '', '', '',
                                                       [self.dm.income_data.id_user], self.dm.id_meeting_owner)
                # msg = json.dumps(message.__dict__)
                self.dm.output_queue.put(message)
                self.dm.send_output()
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeWithList(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "confirmacao" in event and self.dm.income_data.id_user == self.dm.id_meeting_owner:
            # processa aceito
            print("[DialogManagerStates] meeting_owner aceitou a mudança")
            #message = dialog_message.DialogMessage('notify_change_accepted', '', '', '', '', '', '', '', '',
            #                                       self.dm.request_state.income_data.id_user)
            # msg = json.dumps(message.__dict__)
            # self.dm.output_queue.put(message)
            self.dm.send_output()
            self.dm.set_event('master_change')
            if self.dm.request_state:
                return self.dm.request_state
            else:
                return self

        elif "confirmacao" in event:
            # usuario aceitou compromisso
            #seta que user aceitou
            update_query = """UPDATE ListaEncontro 
                                          SET  ACEITOU = 1 
                                          WHERE IDENCONTRO = %s AND IDCLIENTE = %s"""
            cursor = self.dm.con.cursor()
            cursor.execute(update_query, (self.dm.id_meeting, self.income_data.id_user))
            self.dm.con.commit()
            # verifica se ainda existem usuários que não aceitaram
            select_query = """SELECT IDCLIENTE FROM ListaEncontro WHERE ACEITOU = 0 AND IDENCONTRO = %s"""
            cursor.execute(select_query, (self.dm.id_meeting, ))
            lista = cursor.fetchall()
            if len(lista) == 0:
                self.dm.set_event('completed')
                self.dm.notify_all_members(intent='notify_completed')
                return self
            else:  # notifica que usuario aceitou
                self.dm.notify_all_members(intent='notify_response_accept')

            # print("TODO MARCAR COMO ACEITO")

        if "resposta_negativa" in event and self.dm.income_data.id_user == self.dm.id_meeting_owner:
            # notifica solicitante de que alteração foi negada
            message = dialog_message.DialogMessage('notify_change_rejected', '', '', '', '', '', '', '', '',
                                                   self.dm.request_state.income_data.id_user)
            # msg = json.dumps(message.__dict__)
            self.dm.output_queue.put(message)
            self.dm.send_output()
            self.dm.set_next_request()
            # seleciona proximo evento da fila
            if self.dm.request_state is not None:
                self.dm.set_event('master_change')
                return self.dm.request_state
        elif "resposta_negativa" in event:
            # usuario não aceitou compromisso
            # seta que user aceitou
            update_query = """UPDATE ListaEncontro 
                                                      SET  ACEITOU = 2 
                                                      WHERE IDENCONTRO = %s AND IDCLIENTE = %s"""
            cursor = self.dm.con.cursor()
            cursor.execute(update_query, (self.dm.id_meeting, self.income_data.id_user))
            self.dm.con.commit()
            # SELECIONA NOME DO DB PARA EXCLUIR
            # select_query = """SELECT NOME FROM USUARIO WHERE ID = (%s)"""
            # cursor.execute(select_query, (self.income_data.id_user,))
            # nome = cursor.fetchall()
            self.dm.with_list.remove(self.income_data.id_user)
            print("[DialogManagerStates] Nova with_list ", self.dm.with_list)
            # verifica se ainda existem usuários que não aceitaram
            # zero significa que nenhuma decisão foi tomada
            select_query = """SELECT IDCLIENTE FROM ListaEncontro WHERE ACEITOU = 0 AND IDENCONTRO = %s"""
            cursor.execute(select_query, (self.dm.id_meeting, ))
            lista = cursor.fetchall()
            if len(lista) <= 0:
                self.dm.set_event('completed')
                self.dm.notify_all_members('notify_completed')
                # select_query = """SELECT IDCLIENTE FROM LISTAENCONTRO WHERE IDENCONTRO = (%s)"""
                # cursor.execute(select_query, (self.dm.id_meeting,))
                # membros = cursor.fetchall()
                # for membro in membros:
                #     message = dialog_message.DialogMessage('notify', self.dm.commitment, self.dm.with_list,
                #                                            '', self.dm.where, '', self.dm.date, self.dm.hour, '',
                #                                            membro[0])
                #     msg = json.dumps(message.__dict__)
                #     self.dm.og.dispatch_msg(msg)
                return self
            else:
                self.dm.notify_all_members()
                return self

        if "refuse" in event:
            return InfoCompleted(self.dm)


        if "cancel" in event:
            print('[DialogManagerStates] return DialogManager.finish_fsm()')

        if 'completed' in event:
            return self.dm.finish_fsm_sucess()

        return self


class ChangeWhere(State):
    def __init__(self, dm, income_data):
        self.hasInternalEvent = True
        self.dm = dm
        # self.dm.db.set_state('ChangeWhere')
        self.income_data = income_data
        self.__name__ = 'ChangeWhere'

    def on_event(self, event):
        print("[DialogManagerStates] where change accepted")
        if self.income_data:
            if self.income_data.place_known:
                self.dm.where = self.income_data.place_known
            elif self.income_data.place_unknown:
                self.dm.where = self.income_data.place_unknown
            else:
                print("[DialogManagerStates] Place não encontrada na mensagem enviada para mudança de lugar")
                return InfoCompleted(self.dm)
            # atualiza no banco de dados
            update_query = """UPDATE Encontro 
                              SET  ONDE = %s 
                              WHERE ID = %s """ # Altera no db
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.where, self.dm.id_meeting))
            self.dm.con.commit()
            self.dm.notify_all_members('notify_change_accepted')
            # return temp
        self.dm.set_next_request()
        # if self.dm.request_state is not None:
        #     self.dm.set_event('master_change')
        #     return self.dm.request_state

        return InfoCompleted(self.dm)


class ChangeDate(State):
    def __init__(self, dm, income_data):
            self.hasInternalEvent = True
            self.dm = dm
            self.income_data = income_data
            self.__name__ = 'ChangeDate'

    def on_event(self, event):
        if self.income_data.date:
            self.dm.date = self.income_data.date
            # atualiza no banco de dados
            update_query = """UPDATE Encontro 
                              SET  DIA = %s 
                              WHERE ID = %s """  # adiciona no banco de dados
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.date, self.dm.id_meeting))
            self.dm.con.commit()
            self.dm.notify_all_members('notify_change_accepted')
            # return temp
        self.dm.set_next_request()
        # if self.dm.request_state is not None:
        #     self.dm.set_event('master_change')
        #     return self.dm.request_state

        return InfoCompleted(self.dm)


class ChangeWithList(State):
    def __init__(self, dm, income_data):
        self.hasInternalEvent = True
        self.dm = dm
        self.income_data = income_data

    def on_event(self, event):
        if 'add_pessoa' in self.income_data.intent:
            # o primeiro passo para adicionar pessoa é encontrar seu id com base no nome
            for person in self.income_data.person_know:
                # select_query = """SELECT ID FROM USUARIO WHERE NOME LIKE %s ESCAPE '' """
                # print(select_query)
                cursor = self.dm.con.cursor()
                # cursor.execute(select_query, ((person.split(" ")[0].lower() + '%'),))
                # mobile_records = cursor.fetchall()
                # if len(mobile_records) == 1:
                create_query = """INSERT into ListaEncontro (IDENCONTRO, IDCLIENTE, ACEITOU) VALUES (%s, %s, %s) 
                               """
                # iAux = mobile_records[0][0]
                cursor.execute(create_query, (self.dm.id_meeting, person, 0))
                self.dm.con.commit()
                # select_query = """SELECT NOME FROM USUARIO WHERE ID = (%s)"""
                # cursor.execute(select_query, (mobile_records[0][0],))
                # nome = cursor.fetchall()                    self.dm.with_list.append(person)
                self.dm.with_list.append(person)
                # else:
                    # print("[DMS]TODO: MENSAGEM PARA DESAMBIGUAR insert QUERYS NOME %s" %person)
            self.dm.notify_all_members('notify_change_accepted')

        # return InfoCompleted(self.dm)
        else:
            #seleciona usuário
            for person in self.income_data.person_know:
                # select_query = """SELECT ID FROM USUARIO WHERE NOME LIKE %s ESCAPE '' """
                # print(select_query)
                # cursor = self.dm.con.cursor()
                # cursor.execute(select_query, ((person.split(" ")[0].lower() + '%'),))
                # mobile_records = cursor.fetchall()
                # if len(mobile_records) == 1:
                if person in self.dm.with_list:
                    delete_query = """DELETE FROM ListaEncontro  
                                      WHERE IDENCONTRO = %s AND IDCLIENTE = %s"""
                    cursor = self.dm.con.cursor()
                    cursor.execute(delete_query, (self.dm.id_meeting, person))
                    #seleciona nome do db
                    # select_query = """SELECT NOME FROM USUARIO WHERE ID = (%s)"""
                    # cursor.execute(select_query, (mobile_records[0][0],))
                    # nome = cursor.fetchall()
                    self.dm.with_list.remove(person)
                    print("[DMS] Nova with_list ", self.dm.with_list)
                    # else:
                    #     print("[DMS]TODO: MENSAGEM PARA DESAMBIGUAR delete QUERYS NOME %s" %person)
                    self.dm.notify_all_members('notify_change_accepted')
                else:
                    print('[DMFSM] Pessoa não estava na withlist')

        self.dm.set_next_request()
        # if self.dm.request_state is not None:
        #     self.dm.set_event('master_change')
        #     return self.dm.request_state
        return InfoCompleted(self.dm)


class ChangeHour(State):
    def __init__(self, dm, income_data):
        self.hasInternalEvent = True
        self.dm = dm
        self.income_data = income_data

    def on_event(self, event):
        if self.income_data.hour:
            self.dm.hour = self.income_data.hour
            # atualiza no banco de dados
            update_query = """UPDATE Encontro 
                              SET  QUANDO = %s 
                              WHERE ID = %s """  # adiciona no banco de dados
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.hour, self.dm.id_meeting))
            self.dm.con.commit()
            self.dm.notify_all_members('notify_change_accepted')
            # return temp
        self.dm.set_next_request()
        # if self.dm.request_state is not None:
        #     self.dm.set_event('master_change')
        #     return self.dm.request_state

        return InfoCompleted(self.dm)
