import mariadb
from geopy.distance import geodesic

def function():
    print("Hello")
    return


def payment_choice(game, local_money_needed, local_infected_changing, local_dissatisfaction_changing, local_research_progress_changing, local_text):
    if local_money_needed > game.money:
        print("Not enough money to do this choice.")
    else:
        game.money -= local_money_needed
        game.game_turn += 1
        game.infected_population += local_infected_changing
        game.public_dissatisfaction += local_dissatisfaction_changing
        game.research_progress += local_research_progress_changing
        print(f"Spent {local_money_needed} money. Remaining money: {game.money}. {local_text}")


def get_airport_coordinates(icao_code):
    try:
        connection = mariadb.connect(
            host='127.0.0.1',
            port=3306,
            database='test',
            user='root',
            password='root',
            autocommit=True
        )

        sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{icao_code}';"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            latitude, longitude = result
            return latitude, longitude
        else:
            print(f"No coordinates found for ICAO code: {icao_code}")
            return None

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

    finally:
        if connection:
            connection.close()

def distance_between_two(local_coordinates_1, local_coordinates_2):
    if local_coordinates_1 and local_coordinates_2:
        distance = geodesic(local_coordinates_1, local_coordinates_2).kilometers
        return distance
    else:
        return "ERROR: Could not calculate distance because one or both coordinates were not provided."
