import json

import psycopg2

with open("configs/databases.json") as f:
    data = json.load(f)


class DbInterface(object):

    def __init__(self):
        # self.con = psycopg2.connect(user=data["Heroku_db"]["user"],
        #                             password=data["Heroku_db"]["password"],
        #                             host=data["Heroku_db"]["host"],
        #                             port=data["Heroku_db"]["port"],
        #                             database=data["Heroku_db"]["database"])
        self.con = psycopg2.connect(user=data["Local_db"]["user"],
                                    password=data["Local_db"]["password"],
                                    host=data["Local_db"]["host"],
                                    port=data["Local_db"]["port"],
                                    database=data["Local_db"]["database"])

    def connect_to_db(self):
        try:
            cursor = self.con.cursor()
            return cursor
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.con.rollback()
            return None

    def insert(self, user_name, user_slack_id, user_channel, team_id):
        # Adicionar o 'user_slack_id' também
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            postgres_insert_query = """ INSERT INTO usuario (id_slack, Nome, Formacontato, id_team) VALUES (%s,%s, %s, %s)"""
            record_to_insert = (user_slack_id, user_name, user_channel, team_id)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.con.commit()
            cursor.close()
            print("PostgreSQL connection is closed")
            print("-->Novo usuário adicionado ao DB")
            return True
        return False

    def search_user(self, slack_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT ID 
                       FROM USUARIO 
                       WHERE ID_SLACK = (%s)"""
            cursor.execute(query, (slack_id,))
            ids = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if len(ids) == 1:
                print("--> Retorna ID do usuário")
                return ids[0][0]
            return None

    def search_users(self, slack_ids):
        found_members = []
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            for slack_id in slack_ids:
                query = """SELECT ID 
                           FROM USUARIO 
                           WHERE ID_SLACK = (%s)"""
                cursor.execute(query, (slack_id,))
                ids = cursor.fetchall()
                if len(ids) == 1:
                    found_members.append(ids[0][0])
            cursor.close()
            print("PostgreSQL connection is closed")
            print("--> Retorna ID dos contatos")
        return found_members

    def search_users_names(self, users_ids):
        found_members = []
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            for user_id in users_ids:
                if type(user_id) is list:
                    for s_user_id in user_id:
                        query = """SELECT NOME
                                   FROM USUARIO 
                                   WHERE ID = (%s)"""
                        cursor.execute(query, (s_user_id,))
                        ids = cursor.fetchall()
                        if len(ids) == 1:
                            found_members.append(ids[0][0])
                else:
                    query = """SELECT NOME
                               FROM USUARIO 
                               WHERE ID = (%s)"""
                    cursor.execute(query, (user_id,))
                    ids = cursor.fetchall()
                    if len(ids) == 1:
                        found_members.append(ids[0][0])
            cursor.close()
            print("PostgreSQL connection is closed")
            print("--> Retorna ID dos contatos")
        return found_members

    def search_contact(self, user_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT FORMACONTATO 
                       FROM USUARIO 
                       WHERE ID = (%s)"""
            cursor.execute(query, (user_id,))
            contact = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if len(contact) == 1:
                print("--> Retorna canal do usuário")
                return contact[0][0]
            return None

    def search_contact_team_id(self, user_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT ID_TEAM 
                       FROM USUARIO 
                       WHERE ID = (%s)"""
            cursor.execute(query, (user_id,))
            contact = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if len(contact) == 1:
                print("--> Retorna team_id do usuário")
                return contact[0][0]
            return None

    def search_meetings_from_client(self, user_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT distinct(idencontro) 
                       FROM ListaEncontro 
                       WHERE idcliente = (%s)"""
            cursor.execute(query, (user_id,))
            meetings = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if meetings:
                print("--> Retorna encontros do usuário")
                return meetings
            return None

    def search_clients_from_meeting(self, id_meeting):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT distinct(idcliente) 
                       FROM ListaEncontro 
                       WHERE idencontro = (%s)"""
            cursor.execute(query, (id_meeting,))
            clients = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if clients:
                print("Found clients: ", clients)
                print("--> Retorna usuários do encontro")
                return clients
            return None

    def search_mo_from_meeting(self, id_meeting):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT idmeetingowner 
                       FROM encontro 
                       WHERE id = (%s)"""
            cursor.execute(query, (id_meeting,))
            clients = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if clients:
                print("Found clients: ", clients)
                print("--> Retorna usuários do encontro")
                return clients
            return None

    def search_info_from_meeting(self, column, id_meeting):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT {column} 
                       FROM encontro 
                       WHERE id = (%s)""".format(column=column)
            cursor.execute(query, (id_meeting,))
            where = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if where:
                print("--> Retorna {} do encontro".format(column))
                return where
            return None

    def search_meeting_joining_tables(self, column, info, user_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT encontro.ID 
                       FROM encontro INNER JOIN listaencontro 
                       ON encontro.id = listaencontro.idencontro 
                       WHERE encontro.{column} = (%s) AND listaencontro.idcliente = (%s)""".format(column=column)
            cursor.execute(query, ("{"+info+"}", user_id,))
            meetings = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if meetings:
                return meetings
            return []

    def search_all_meeting_info(self, meeting_id):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """SELECT IDMEETINGOWNER, ONDE, QUANDO, OQUE, DIA 
                       FROM ENCONTRO 
                       WHERE ID = (%s)"""
            cursor.execute(query, (meeting_id,))
            info = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if info:
                return info
            return []

    def update_meeting(self, meeting_id, infos):
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            query = """UPDATE LISTAENCONTRO SET ACEITOU = %s 
                       WHERE IDENCONTRO = %s and IDCLIENTE <> %s"""
            cursor.execute(query, (0, meeting_id, infos[0][0]))
            cursor.close()
            self.con.commit()
            print("PostgreSQL connection is closed")
