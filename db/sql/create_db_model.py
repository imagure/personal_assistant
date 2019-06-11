import psycopg2
import json

with open("db/sql/databases.json") as f:
    data = json.load(f)


def create_model(environment):
    try:
        if environment == 'heroku':
            connection = psycopg2.connect(user=data["Heroku_db"]["user"],
                                          password=data["Heroku_db"]["password"],
                                          host=data["Heroku_db"]["host"],
                                          port=data["Heroku_db"]["port"],
                                          database=data["Heroku_db"]["database"])
        else:
            connection = psycopg2.connect(user=data["Local_db"]["user"],
                                          password=data["Local_db"]["password"],
                                          host=data["Local_db"]["host"],
                                          port=data["Local_db"]["port"],
                                          database=data["Local_db"]["database"])
        cursor = connection.cursor()
        try:
            drop_table_query = '''DROP TABLE usuario'''
            cursor.execute(drop_table_query)
            connection.commit()
            drop_table_query = '''DROP TABLE ItemAgenda'''
            cursor.execute(drop_table_query)
            connection.commit()
            drop_table_query = '''DROP TABLE Encontro'''
            cursor.execute(drop_table_query)
            connection.commit(),

            drop_table_query = '''DROP TABLE ListaEncontro'''
            cursor.execute(drop_table_query)
            connection.commit()

        except(Exception, psycopg2.Error) as error:
            print("Não havia tabela no db", error)
            connection.rollback()
        # cria tabela de usuário
        create_table_query = '''CREATE TABLE usuario 
            (ID SERIAL PRIMARY KEY,
            ID_SLACK TEXT NOT NULL,
            NOME TEXT NOT NULL ,
            FORMACONTATO TEXT NOT NULL,
            ID_TEAM TEXT NOT NULL)'''
        try:
            cursor.execute(create_table_query)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error", error)
            connection.rollback()
        create_table_query = '''CREATE TABLE ItemAgenda 
                (ID SERIAL PRIMARY KEY,
                IDDONO INT  NOT NULL ,
                IDCONTATO INT  NOT NULL)'''
        try:
            cursor.execute(create_table_query)
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error", error)
            connection.rollback()
        create_table_query = '''CREATE TABLE ListaEncontro 
                (ID SERIAL PRIMARY KEY,
                IDENCONTRO INT NOT NULL,
                IDCLIENTE INT NOT NULL,
                ACEITOU INT)'''  # ACEITOU = {0 - Não aceito, 1 - Aceitou, 2 - Não aceitou }
        try:
            cursor.execute(create_table_query)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error", error)
            connection.rollback()
        create_table_query = '''CREATE TABLE Encontro 
                 (ID SERIAL PRIMARY KEY ,
                 ONDE TEXT [],
                 QUANDO TEXT [],
                 DIA TEXT [],
                 OQUE TEXT [],
                 IDMEETINGOWNER INT NOT NULL,
                 ESTADO TEXT)'''
        try:
            cursor.execute(create_table_query)
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error", error)
            connection.rollback()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    print("Digite 'heroku' para criar modelo no DB da amazon.")
    environment = input(">")
    create_model(environment)
