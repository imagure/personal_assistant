from dialog_manager.State import *
from dialog_manager.initial_info_fsm import initial_info_fsm
import psycopg2

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
                print("id_criado", self.dm.id_meeting)
                postgres_insert_query = """INSERT INTO ListaEncontro (IDENCONTRO, IDCLIENTE)
                                           VALUES(%s, %s)"""
                #adiciona meeting owner a lista de eventos
                cursor.execute(postgres_insert_query, (self.dm.id_meeting, self.income_data.id_user))
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
            # Lembrar de tirar isso depois
            print("RESETANDO PARA IDLE! TIRAR DEPOIS!!")
            self.dm.with_list = []
            self.dm.where = []
            self.dm.when = []
            self.dm.date = []
            self.dm.commitment = []
            self.income_data = []
            # return InfoCompleted(self.dm) # temporariamente retirado
            return Idle('', self.dm)
        self.ISM.on_event(event)
        return self


class InfoCompleted(State):
    def __init__(self, dm):
        self.hasInternalEvent = True
        print("informacoes basicas coletadas")
        self.dm = dm

    def on_event(self, event):
        if event == "change_where":  # intent event
            return ChangeWhere(self.dm)
        if event == "change_date":
            return ChangeDate(self.dm)
        if event == "change_with_list":
            return ChangeWithList(self.dm)
        if event == "refuse":
            return InfoCompleted(self.dm)
        if event == "change_hour":
            return ChangeHour(self.dm)
        if event == "cancel":
            print('return DialogManager.finish_fsm()')
        if event == "internal":
            print('return DialogManager.finish_fsm_sucess()')
        return self


class ChangeWhere(State):
    def __init__(self, dm):
        self.hasInternalEvent = True
        self.dm = dm

    def on_event(self, event):
        if event == "accept":
            return InfoCompleted(self.dm)
        if event == "reject":
            return InfoCompleted(self.dm)
        return self


class ChangeDate(State):
    class ChangeWhere(State):
        def __init__(self, dm):
            self.hasInternalEvent = True
            self.dm = dm

    def on_event(self, event):
        if event == "accept":
            return InfoCompleted(self.dm)
        if event == "reject":
            return InfoCompleted(self.dm)
        return self


class ChangeWithList(State):
    class ChangeWhere(State):
        def __init__(self, dm):
            self.hasInternalEvent = True
            self.dm = dm

    def on_event(self, event):
        if event == "accept":
            return InfoCompleted(self.dm)
        if event == "reject":
            return InfoCompleted(self.dm)
        return self


class ChangeHour(State):
    class ChangeWhere(State):
        def __init__(self, dm):
            self.hasInternalEvent = True
            self.dm = dm

    def on_event(self, event):
        if event == "accept":
            return InfoCompleted(self.dm)
        if event == "reject":
            return InfoCompleted(self.dm)
        return self
