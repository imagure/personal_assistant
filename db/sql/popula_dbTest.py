import psycopg2
import json

with open("db/sql/databases.json") as f:
    data = json.load(f)

# ricardo.imagure:                              UHG2AKKEK   DHCH9G02U
# Ricardo Imagure/ricardo.imagure092 "Camargo"  UHG8PNEVB   DHHBT90B0
# Mateus Ramos Vendramini:                      UHG2FGQQ5   CKAJF4JSK(temp)


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

        record_to_insert = ('Ricardo Imagure', 'UHG2AKKEK', 'DHCH9G02U')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = ('Ricardo Camargo', 'UHG8PNEVB', 'DHHBT90B0')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = ('Mateus Vendramini', 'UHG2FGQQ5', 'CKAJF4JSK')
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


if __name__ == '__main__':
    print("Digite 'heroku' para popular DB da amazon.")
    environment = input(">")
    populate(environment)
