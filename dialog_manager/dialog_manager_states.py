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
        self.income_data = income_data

    def on_event(self, event):
        # any msg received from the semantizer will make the FSM go to InitialInfo
        if "marcar_compromisso" in event:
            print("Indo para estado de InitialInfo")
            if self.income_data.id_user:
                postgres_insert_query = """ INSERT INTO Encontro (IDMEETINGOWNER) VALUES (%d) RETURNING ID """ % self.income_data.id_user
                print(postgres_insert_query)
                cursor = self.dm.con.cursor()
                cursor.execute(postgres_insert_query)
                self.dm.con.commit()
                self.dm.id_meeting = cursor.fetchone()[0]
                self.dm.id_meeting_owner = self.income_data.id_user
                print("id_criado", self.dm.id_meeting)
                # considera que o meeting owner sempre aceita o encontro
                postgres_insert_query = """INSERT INTO ListaEncontro (IDENCONTRO, IDCLIENTE, ACEITOU)
                                           VALUES(%s, %s, %s)"""
                # adiciona meeting owner a lista de eventos
                cursor.execute(postgres_insert_query, (self.dm.id_meeting, self.income_data.id_user, 1))
                self.dm.con.commit()
                return InitialInfo(self.dm)
            else:
                print("Usuario não identificado")
                return self
        elif "add_pessoa" in event:
            print("TODO: Tratamento para localizar encontro")
        return self


class InitialInfo(State):
    def __init__(self,  dm):
        self.hasInternalEvent = True
        self.ISM = initial_info_fsm.InitialInfoSM(dm)
        self.dm = dm

    def on_event(self, event):
        if event is "info_finished":
            return InfoCompleted(self.dm) # temporariamente retirado
            # Lembrar de tirar isso depois
            print("RESETANDO PARA IDLE! TIRAR DEPOIS!!")
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
        print("informacoes basicas coletadas")
        self.dm = dm

    def on_event(self, event):
        if "remarcar_compromisso" in event:
            if self.income_data.hour != []:
                event = ['change_hour']
                self.income_data.intent = ['change_hour']
            elif self.income_data.date != []:
                event = ['change_date']
                self.income_data.intent = event
        if "mudar_lugar" in event:  # intent event
            if self.dm.request_queue.empty() and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeWhere(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage(event, [''], '', '', self.income_data.place_known,
                                                       self.income_data.place_unknown, '', '',
                                                       self.income_data.id_user, self.dm.id_meeting_owner)
                msg = json.dumps(message.__dict__)
                self.dm.og.dispatch_msg(msg)
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeWhere(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

            # return ChangeWhere(self.dm)
        if "change_date" in event:
            if self.dm.request_queue.empty() and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeDate(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage(event, [''], '',
                                                       '', '', '', self.income_data.date, '',
                                                       self.income_data.id_user, self.dm.id_meeting_owner)
                msg = json.dumps(message.__dict__)
                self.dm.og.dispatch_msg(msg)
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeDate(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "change_hour" in event:
            if self.dm.request_queue.empty() and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeHour(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage(event, [''], '',
                                                       '', '', '', '', self.income_data.hour,
                                                       self.income_data.id_user, self.dm.id_meeting_owner)
                msg = json.dumps(message.__dict__)
                self.dm.og.dispatch_msg(msg)
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeHour(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "excl_pessoa" in event or "add_pessoa" in event:
            if self.dm.request_queue.empty() and self.dm.income_data.id_user != self.dm.id_meeting_owner:
                # Popula request state
                self.dm.request_state = ChangeWithList(self.dm, self.dm.income_data)
                # envia mensagem de solicitação para o meeting owner
                # por enquanto assume que não chegará mensagem para excluir sem pessoa a ser excluida
                message = dialog_message.DialogMessage(event, [''], self.income_data.person_know,
                                                       self.income_data.person_unknown, '', '', '', '',
                                                       self.income_data.id_user, self.dm.id_meeting_owner)
                msg = json.dumps(message.__dict__)
                self.dm.og.dispatch_msg(msg)
            elif self.dm.income_data.id_user == self.dm.id_meeting_owner:
                self.dm.set_event('master_change')
                return ChangeWithList(self.dm, self.dm.income_data)
            else:
                # não foi possível processar pedido de alteração agora
                # armazena para mais tarde
                self.dm.request_queue.put(self.dm.income_data)

        if "confirmacao" in event and self.dm.income_data.id_user == self.dm.id_meeting_owner:
            # processa aceito
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
            list = cursor.fetchall()
            if len(list) == 0:
                self.dm.set_event('completed')
                self.dm.notify_all_members()
                return self

            print("TODO MARCAR COMO ACEITO")

        if "reject" in event and self.dm.income_data.id_user == self.dm.id_meeting_owner:
            # notifica solicitante de que alteração foi negada
            message = dialog_message.DialogMessage('change_refused', '', '', '', '', '', '', '', '',
                                                   self.dm.request_state.income_data.id_user)
            msg = json.dumps(message.__dict__)
            self.dm.og.dispatch_msg(msg)
        elif "reject" in event:
            # usuario não aceitou compromisso
            # seta que user aceitou
            update_query = """UPDATE ListaEncontro 
                                                      SET  ACEITOU = 2 
                                                      WHERE ID = %s """
            cursor = self.dm.conn.cursor()
            cursor.execute(update_query, (self.dm.id_meeting,))
            self.dm.con.commit()
            # verifica se ainda existem usuários que não aceitaram
            # zero significa que nenhuma decisão foi tomada
            select_query = """SELECT IDUSER FROM ListaEncontro WHERE ACEITOU <> 0 AND IDENCONTRO = %s"""
            cursor.execute(select_query, (self.dm.id_meeting, ))
            list = cursor.fetchall()
            if len(list) <= 0:
                self.dm.set_event('completed')
                select_query = """SELECT IDUSER FROM LISTAENCONTRO WHERE IDENCONTRO = (%s)"""
                cursor.execute(select_query, (self.dm.id_meeting,))
                membros = cursor.fetchall()
                for membro in membros:
                    message = dialog_message.DialogMessage('notify', self.dm.commitment, self.dm.with_list,
                                                           '', self.dm.where, '', self.dm.date, self.dm.hour, '',
                                                           membro[0])
                    msg = json.dumps(message.__dict__)
                    self.dm.og.dispatch_msg(msg)
                return self

        if "refuse" in event:
            return InfoCompleted(self.dm)


        if "cancel" in event:
            print('return DialogManager.finish_fsm()')

        if 'completed' in event:
            return self.dm.finish_fsm_sucess()

        return self


class ChangeWhere(State):
    def __init__(self, dm, income_data):
        self.hasInternalEvent = True
        self.dm = dm
        self.income_data = income_data

    def on_event(self, event):
        print("where changed")
        if self.income_data:
            if self.income_data.place_known:
                self.dm.where = self.income_data.place_known
            elif self.income_data.place_unknown:
                self.dm.where = self.income_data.place_unknown
            else:
                print("Place não encontrada na mensagem")
                return InfoCompleted(self.dm)
            # atualiza no banco de dados
            update_query = """UPDATE Encontro 
                              SET  ONDE = %s 
                              WHERE ID = %s """ # Altera no db
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.where, self.dm.id_meeting))
            self.dm.con.commit()
            self.dm.notify_all_members()
            # return temp
        self.dm.set_next_request()

        return InfoCompleted(self.dm)


class ChangeDate(State):
    def __init__(self, dm, income_data):
            self.hasInternalEvent = True
            self.dm = dm
            self.income_data = income_data

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
            self.dm.notify_all_members()
            # return temp
        self.dm.set_next_request()

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
                select_query = """SELECT ID FROM USUARIO WHERE NOME LIKE %s ESCAPE '' """
                #print(select_query)
                cursor = self.dm.con.cursor()
                cursor.execute(select_query, ((person.split(" ")[0].lower() + '%'),))
                mobile_records = cursor.fetchall()
                if len(mobile_records) == 1:
                    create_query = """INSERT into ListaEncontro (IDENCONTRO, IDCLIENTE, ACEITOU) VALUES (%s, %s, %s) 
                                    """
                    # iAux = mobile_records[0][0]
                    cursor.execute(create_query, (self.dm.id_meeting, mobile_records[0][0], 0))
                    self.dm.con.commit()
                    self.dm.with_list.append(person)
                else:
                    print("TODO: MENSAGEM PARA DESAMBIGUAR insert QUERYS NOME %s" %person)
            self.dm.notify_all_members()

        # return InfoCompleted(self.dm)
        else:
            #seleciona usuário
            for person in self.income_data.person_know:
                select_query = """SELECT ID FROM USUARIO WHERE NOME LIKE %s ESCAPE '' """
                #print(select_query)
                cursor = self.dm.con.cursor()
                cursor.execute(select_query, ((person.split(" ")[0].lower() + '%'),))
                mobile_records = cursor.fetchall()
                if len(mobile_records) == 1:
                    delete_query = """DELETE FROM ListaEncontro WHERE IDENCONTRO = %s AND IDCLIENTE = %s """
                    cursor.execute(delete_query, (self.dm.id_meeting, mobile_records[0][0]))
                    self.dm.with_list.remove(person)
                    print("Nova with_list ", self.dm.with_list)

                else:
                    print("TODO: MENSAGEM PARA DESAMBIGUAR delete QUERYS NOME %s" %person)
            self.dm.notify_all_members()

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
            self.dm.notify_all_members()
            # return temp
        self.dm.set_next_request()

        return InfoCompleted(self.dm)
