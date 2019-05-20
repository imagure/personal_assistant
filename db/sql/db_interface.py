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

    def insert(self, user_name, user_slack_id, user_channel):
        # Adicionar o 'user_slack_id' também
        cursor = self.connect_to_db()
        if cursor:
            print("PostgreSQL connection is opened")
            postgres_insert_query = """ INSERT INTO usuario (id_slack, Nome, Formacontato) VALUES (%s,%s, %s)"""
            record_to_insert = (user_slack_id, user_name, user_channel)
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
            query = """SELECT ID FROM USUARIO WHERE FORMACONTATO = (%s)"""
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
                query = """SELECT ID FROM USUARIO WHERE FORMACONTATO = (%s)"""
                cursor.execute(query, (slack_id,))
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
            query = """SELECT FORMACONTATO FROM USUARIO WHERE ID = (%s)"""
            cursor.execute(query, (user_id,))
            contact = cursor.fetchall()
            cursor.close()
            print("PostgreSQL connection is closed")
            if len(contact) == 1:
                print("--> Retorna canal do usuário")
                return contact[0][0]
            return None
