import json

import psycopg2
from Crypto.Cipher import DES

with open("db/sql/databases.json") as f:
    data = json.load(f)

# ricardo.imagure:                              UHG2AKKEK   DHCH9G02U
# Ricardo Imagure/ricardo.imagure092 "Camargo"  UHG8PNEVB   DHHBT90B0
# Mateus Ramos Vendramini:                      UHG2FGQQ5   DK2RKUFSN(temp)

des = DES.new('01234567', DES.MODE_ECB)


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

        postgres_insert_query = """ INSERT INTO usuario ( Nome, id_slack, Formacontato, id_team) VALUES (%s,%s,%s,%s)"""

        record_to_insert = ('Ricardo Imagure', 'UHG2AKKEK', 'DHCH9G02U', 'THGD0P2GN')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = ('Ricardo Camargo', 'UKHJ85Q0N', 'CLGTSL4FR', 'TKE8JAR1N')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        record_to_insert = ('Mateus Vendramini', 'UK2RKU77U', 'DK2RKUFSN', 'TKE8JAR1N')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        postgres_insert_query = """INSERT INTO SlackWorkspaces (team_id, token) VALUES (%s,%s)"""

        token_input = des.encrypt('xoxp-594442784566-594078665495-593343524389-fecda7db64b17348c9ac1aa83970284b0000')
        print("token 1: ", token_input)
        print("token 1: ", des.decrypt(token_input)[0:-4].decode('utf-8'))
        record_to_insert = ('THGD0P2GN', psycopg2.Binary(token_input))
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

        token_input = des.encrypt('xoxp-660290365056-663620194022-662310731236-9de51b6765066f83373af35b2c80a2940000')
        print("token 2: ", token_input)
        print("token 2: ", des.decrypt(token_input)[0:-4].decode('utf-8'))
        record_to_insert = ('TKE8JAR1N', psycopg2.Binary(token_input))
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
