import psycopg2
import json

with open("databases.json") as f:
    data = json.load(f)

try:
    # connection = psycopg2.connect(user=data["Heroku_db"]["user"],
    #                               password=data["Heroku_db"]["password"],
    #                               host=data["Heroku_db"]["host"],
    #                               port=data["Heroku_db"]["port"],
    #                               database=data["Heroku_db"]["database"])
    # print("TIRAR QUANDO FOR DAR DEPLOY!!!!!11!!!!1")
    connection = psycopg2.connect(user="user",
                                  password="Toalhamesa",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="dev")
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
        FORMACONTATO TEXT NOT NULL)'''
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
             ONDE TEXT ,
             QUANDO TEXT ,
             DIA TEXT,
             OQUE TEXT ,
             IDMEETINGOWNER INT NOT NULL)'''
    try:
        cursor.execute(create_table_query)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error", error)
        connection.rollback()
    print("Populando usuários")

    postgres_insert_query = """ INSERT INTO usuario ( Nome, id_slack, Formacontato) VALUES (%s,%s,%s)"""
    record_to_insert = ('carlinhos', 'UHG2AKKEK', 'CHPMBMG94')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('mateus vendramini', 'UHG2FGQQ5', 'DHGQ8GVEK')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('ricardo imagure', 'UHG2AKKEK', 'CHNNMA24D')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('marcos barreto', 'UHG2FGQQ5', 'CHQCV963Y')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('erika imagure', 'UHG2AKKEK', 'CHE8333G9')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('bruno ribeiro', 'UHG2FGQQ5', 'CHCH9GG0Y')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    print("Populando Agendas")
    postgres_insert_query = """ INSERT INTO ItemAgenda ( IDDONO, IDCONTATO) VALUES (%s,%s)"""
    record_to_insert = (1, 2)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (1, 3)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (1, 4)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (4, 1)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (1, 5)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (5, 1)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (2, 1)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (2, 3)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (3, 1)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = (3, 2)
    cursor.execute(postgres_insert_query, record_to_insert)
    print(record_to_insert)
    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
    connection.rollback()
finally:
    # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
