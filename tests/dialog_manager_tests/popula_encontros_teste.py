import psycopg2
import json

with open("db/sql/databases.json") as f:
    data = json.load(f)


def populate_encontro():

    try:
        connection = psycopg2.connect(user=data["Local_db"]["user"],
                                      password=data["Local_db"]["password"],
                                      host=data["Local_db"]["host"],
                                      port=data["Local_db"]["port"],
                                      database=data["Local_db"]["database"])
        cursor = connection.cursor()

        print("Populando usuários")

        postgres_insert_query = """ INSERT INTO encontro ( onde, quando, dia, oque, idmeetingowner) VALUES (%s,%s,%s, %s, %s)"""

        record_to_insert = (['office'], ['09:00:00'], ['2019-09-28'], ['reunion'], 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (['bar'], ['20:00:00'], ['2019-09-04'], ['party'], 2)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (['cinema'], ['18:00:00'], ['2019-11-22'], ['meeting'], 3)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def populate_listaencontro():
    try:
        connection = psycopg2.connect(user=data["Local_db"]["user"],
                                      password=data["Local_db"]["password"],
                                      host=data["Local_db"]["host"],
                                      port=data["Local_db"]["port"],
                                      database=data["Local_db"]["database"])
        cursor = connection.cursor()

        print("Populando usuários")

        postgres_insert_query = """ INSERT INTO listaencontro ( idencontro, idcliente, aceitou) VALUES (%s,%s,%s)"""

        record_to_insert = (1, 1, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (1, 2, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (1, 3, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (2, 1, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (2, 2, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (2, 3, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (3, 1, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (3, 2, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = (3, 3, 1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
