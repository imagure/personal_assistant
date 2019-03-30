import psycopg2
import json

with open("configs/databases.json") as f:
    data = json.load(f)

try:
    #senha = input("Digite senha do db")
    connection = psycopg2.connect(user=data["Heroku_db"]["user"],
                                  password=data["Heroku_db"]["password"],
                                  host=data["Heroku_db"]["host"],
                                  port=data["Heroku_db"]["port"],
                                  database=data["Heroku_db"]["database"])
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
            IDCLIENTE INT NOT NULL)'''
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

    postgres_insert_query = """ INSERT INTO usuario ( Nome, Formacontato) VALUES (%s,%s)"""
    record_to_insert = ('carlinhos', '{"email"="carlinhos@gmail.com"}')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('mateus vendramini', 'DHGQ8GVEK')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('ricardo imagure', 'DHCH9G02U')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

    record_to_insert = ('canal teste', 'CHCH9GG0Y')
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
