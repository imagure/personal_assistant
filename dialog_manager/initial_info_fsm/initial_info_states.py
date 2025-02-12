from dialog_manager.State import *
from dialog_message.dialog_message import *


class GetWHAT(State):
    """
    Estado para procurar with_list
    """
    def __init__(self, dm):
        self.dm = dm
        self.found = False

    def on_event(self, event):
        print("What Event")
        temp = GetWithList(self.dm)
        if self.dm.commitment == [] and self.dm.income_data.commitment != []:
            self.dm.commitment = self.dm.income_data.commitment
            # adiciona no banco de dados
            update_query = """UPDATE Encontro 
                              SET OQUE = %s 
                              WHERE ID = %s """
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.commitment, self.dm.id_meeting))
            self.dm.con.commit()

            self.dm.set_internal_event(self.dm.income_data)
            print('what na entrada')
            self.found = True
            return temp
        elif self.dm.commitment == []:
            print("NAO ENTENDI WHAT")
            message = DialogMessage('ask_what', '', [], '', '', '', '', '', '', self.dm.income_data.id_user)
            self.dm.output_queue.put(message)
        print('what já estava presente?')
        self.dm.set_internal_event(self.dm.income_data)
        return temp


class GetWithList(State):
    """
    Estado para procurar with_list
    """
    def __init__(self, dm):
        self.dm = dm

    def on_event(self, event):
        print("[IFFSM]WithList")
        temp = GetWhen(self.dm)
        # comentei self.dm.with_list == [] and
        if (self.dm.income_data.person_know != [] or (self.dm.income_data.person_unknown != [])):
            if self.dm.income_data.person_unknown != [] and self.dm.income_data.person_unknown != "":
                message = DialogMessage('ask_who', '', '', self.dm.income_data.person_unknown, '', '', '', '', '',
                                        self.dm.income_data.id_user)
                self.dm.output_queue.put(message)
            for person in self.dm.income_data.person_know:
                if isinstance(person, list):
                    message = DialogMessage('desambiguate', '',  [person], '', '', '', '', '', '',
                                            self.dm.income_data.id_user)
                    self.dm.output_queue.put(message)
                else:
                    # here person should be a string
                    # select_query = """SELECT ID FROM USUARIO WHERE NOME LIKE %s ESCAPE '' """
                    # print(select_query)
                    cursor = self.dm.con.cursor()
                    # cursor.execute(select_query, ((person.split(" ")[0].lower() + '%'), )) # (person.split(" ")[0].lower(),))
                    # mobile_records = cursor.fetchall()
                    #if len(mobile_records) == 1:
                        # primeiro verifica se usuario já não está no encontro
                    select_query = """SELECT ID FROM ListaEncontro WHERE IDENCONTRO = %s AND IDCLIENTE = %s"""
                    cursor.execute(select_query, (self.dm.id_meeting, person))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        create_query = """INSERT into ListaEncontro (IDENCONTRO, IDCLIENTE, ACEITOU) VALUES (%s, %s, %s) 
                        """
                        # iAux = mobile_records[0][0]
                        cursor.execute(create_query, (self.dm.id_meeting, person, 0))
                        self.dm.con.commit()
                        # adiciona nome cadastrado no banco de dados
                        # select_query = """SELECT NOME FROM USUARIO WHERE ID = (%s)"""
                        # cursor.execute(select_query, (mobile_records[0][0], ))
                        # nomes = cursor.fetchall()
                        self.dm.with_list.append(person)
                            # self.dm.with_list.append(self.dm.income_data.person_unknown)
                    # else:
                    #    message = DialogMessage('desambiguate', '', '', [person], '', '', '', '', '',
                    #                            self.dm.income_data.id_user)
                    #    self.dm.output_queue.put(message)

            self.dm.set_internal_event(self.dm.income_data)
            return temp
        # menor que um pois pode ter apenas o MO
        elif len(self.dm.with_list) <= 1:
            print("[IFFSM] NAO ENTENDI WithList")
            message = DialogMessage('ask_withlist', '', [], '', '', '', '', '', '', self.dm.income_data.id_user)
            self.dm.output_queue.put(message)
        self.dm.set_internal_event(self.dm.income_data)
        return temp


class GetWhen(State):
    """
    Estado para procurar with_list
    """
    def __init__(self, dm):
        self.dm = dm

    def on_event(self, event):
        print("When event")
        temp = GetWhere(self.dm)
        if self.dm.date == [] and self.dm.income_data.date != []:
            self.dm.date = self.dm.income_data.date
            # adiciona no banco de dados
            update_query = """UPDATE Encontro 
                           SET  DIA = %s 
                           WHERE ID = %s """
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.date, self.dm.id_meeting))
            self.dm.con.commit()
            print('hour já estava presente')
            # return temp
        if self.dm.hour == [] and self.dm.income_data.hour != []:
            self.dm.hour = self.dm.income_data.hour
            # adiciona no banco de dados
            update_query = """UPDATE Encontro 
                              SET  QUANDO = %s 
                              WHERE ID = %s """
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.hour, self.dm.id_meeting))
            self.dm.con.commit()
            print('date já estava presente')
            # return temp
        if self.dm.date == [] or self.dm.date == "{}":
            print("NAO ENTENDI date")
            message = DialogMessage('ask_date', '', [], '', '', '', '', '', '', self.dm.income_data.id_user)
            self.dm.output_queue.put(message)
        if self.dm.hour == [] or self.dm.hour == "{}":
            print("NAO ENTENDI hour")
            message = DialogMessage('ask_hour', '', [], '', '', '', '', '', '', self.dm.income_data.id_user)
            self.dm.output_queue.put(message)
        self.dm.set_internal_event(self.dm.income_data)
        return temp


class GetWhere(State):
    """
    Estado para procurar with_list
    """

    def __init__(self, dm):
        self.dm = dm

    def on_event(self, event):
        print("Where event")
        if self.dm.where == [] and(self.dm.income_data.place_known != []
                                   or self.dm.income_data.place_unknown != []):
            if self.dm.income_data.place_known:
                self.dm.where = self.dm.income_data.place_known
            else:
                self.dm.where = self.dm.income_data.place_unknown
            # adiciona no banco de dados
            update_query = """UPDATE Encontro 
                                          SET ONDE = %s 
                                          WHERE ID = %s """
            cur = self.dm.con.cursor()
            cur.execute(update_query, (self.dm.where, self.dm.id_meeting))
            self.dm.con.commit()

            if self.dm.output_queue.qsize() == 0:
                # finished, will notify all users in the meeting
                # user_query = """SELECT IDCLIENTE from ListaEncontro WHERE IDENCONTRO = (%s)"""
                # cur = self.dm.con.cursor()
                # cur.execute(user_query, (self.dm.id_meeting,))
                # convidadosId = cur.fetchall()
                for convidadoId in self.dm.with_list:
                    if convidadoId != self.dm.id_meeting_owner:
                        message = DialogMessage('invite', self.dm.commitment, self.dm.with_list, '',
                                                self.dm.where, '', self.dm.date, self.dm.hour, '',
                                                convidadoId)  # criar meetingowner
                    else:
                        message = DialogMessage('notify_initial_info', self.dm.commitment, self.dm.with_list, '',
                                                self.dm.where, '', self.dm.date, self.dm.hour, '',
                                                convidadoId)  # criar meetingowner
                    self.dm.output_queue.put(message)
                self.dm.send_output()
                self.dm.set_event("info_finished")
                return self
            else:
                self.dm.send_output()
                return GetWHAT(self.dm)
        elif self.dm.where == []:
            print("NAO ENTENDI GetWhere")
            message = DialogMessage('ask_where', '', [], '', '', '', '', '', '', self.dm.income_data.id_user)
            self.dm.output_queue.put(message)
        elif self.dm.output_queue.qsize() == 0:
            # user_query = """SELECT IDCLIENTE from ListaEncontro WHERE IDENCONTRO = (%s)"""
            # cur = self.dm.con.cursor()
            # cur.execute(user_query, (self.dm.id_meeting,))
            # convidadosId = cur.fetchall()
            for convidadoId in self.dm.with_list:
                if convidadoId != self.dm.id_meeting_owner:
                    message = DialogMessage('invite', self.dm.commitment, self.dm.with_list, '',
                                        self.dm.where, '', self.dm.date, self.dm.hour, '',
                                        convidadoId)  # criar meetingowner
                else:
                    message = DialogMessage('notify_initial_info', self.dm.commitment, self.dm.with_list, '',
                                            self.dm.where, '', self.dm.date, self.dm.hour, '',
                                            convidadoId)  # criar meetingowner

                self.dm.output_queue.put(message)
            print("coleta de informacoes basicas acabou")
            self.dm.set_event("info_finished")
            self.dm.send_output()
            return self

        self.dm.send_output()
        return GetWHAT(self.dm)



