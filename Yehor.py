import mariadb
from geopy.distance import geodesic
import database_manager as db
import main
import time

def run_sql_from_file(sql_file_path: object = 'choices.sql') -> object:
    try:
        with open(sql_file_path, 'r') as file:
            sql_query = file.read()

        return db.run(sql_query)
    except FileNotFoundError:
        print(f"Error: File {sql_file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Load choices directly from the database
def load_choices_from_db():
    query = "SELECT name, money_needed, infected_changing, dissatisfaction_changing, research_progress_changing, text, sql_query FROM choices;"
    return db.run(query)

# Convert database result row to tuple (not necessary since SQL result is already a tuple)
def convert_choice_to_tuple(db_choice_row):
    return db_choice_row

def function():
    print("Hello")
    return

# Function to handle making a choice
def payment_choice(game, choice_tuple):
    name, money_needed, infected_changing, dissatisfaction_changing, research_progress_changing, text, sql_query = choice_tuple

    if money_needed > game.money:
        print("Not enough money to do this choice.")
    else:
        game.money -= money_needed
        game.game_turn += 1

        if infected_changing != 0:
            game.infected_population += infected_changing
            print(f"Infected population changed by {infected_changing}. Now it is {game.infected_population}")
            time.sleep(1)

        if dissatisfaction_changing != 0:
            game.public_dissatisfaction += dissatisfaction_changing
            print(f"Public dissatisfaction changed by {dissatisfaction_changing}. Now it is {game.public_dissatisfaction}")
            time.sleep(1)

        if research_progress_changing != 0:
            game.research_progress += research_progress_changing
            print(f"Research progress changed by {research_progress_changing}. Now it is {game.research_progress}")
            time.sleep(1)

        if sql_query != "":
            game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{game.name}'")[0][0]
            string_query = (f"UPDATE airport_info "
                            f"{sql_query} " #SET closed = 1
                            f"WHERE game_id = {game_id}")
            #Update ... SET closed = 1

            db.run(string_query)

        if text != "":
            print(text)

def get_airport_coordinates(icao_code):
    try:
        connection = mariadb.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
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

def distance_between_two(coord_1, coord_2):
    if coord_1 and coord_2:
        distance = geodesic(coord_1, coord_2).kilometers
        return distance
    else:
        return 999999999  # can be changed
