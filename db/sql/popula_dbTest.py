import psycopg2
import json

with open("db/sql/databases.json") as f:
    data = json.load(f)


def populate(environment):
    try:
        if environment == "heroku":
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
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    print("Digite 'heroku' para popular DB da amazon.")
    environment = input(">")
    populate(environment)
