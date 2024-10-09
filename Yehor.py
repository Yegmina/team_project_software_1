import mariadb
import mysql
from geopy.distance import geodesic
import database_manager as db
import main
import time
import mysql.connector
import Colours

def run_sql_from_file(sql_file_path: object = 'choices.sql') -> object:
    try:
        with open(sql_file_path, 'r') as file:
            sql_query = file.read()

        return db.run(sql_query)
    except FileNotFoundError:
        print(Colours.RED + f"Error: File {sql_file_path} not found." + Colours.RESET) #red
        return None
    except Exception as e:
        print(Colours.RED + f"An error occurred: {e}" + Colours.RESET) #red
        return None

# Load choices directly from the database
def load_choices_from_db():
    query = "SELECT name, money_needed, infected_changing, dissatisfaction_changing, research_progress_changing, text, sql_query, infection_rate FROM choices;"
    return db.run(query)

# Convert database result row to tuple (not necessary since SQL result is already a tuple)
def convert_choice_to_tuple(db_choice_row):
    return db_choice_row

# Function to handle making a choice
def payment_choice(game, choice_tuple):
    name, money_needed, infected_changing, dissatisfaction_changing, research_progress_changing, text, sql_query, infection_rate  = choice_tuple

    game.game_turn += 1
    if game.game_turn % 5 == 1:
        if game.infected_population<80:
            print(f"Infected is now {int(game.infected_population)}")
        else:
            print(Colours.RED + f"Attention!!! The world's population is almost all infected - {game.infected_population}" + Colours.RESET)
        time.sleep(1)

    # Ensure the player has enough money to make the choice
    if money_needed > game.money:
        print(Colours.BRIGHT_YELLOW + "Not enough money, so you skipped the choice this turn!" + Colours.RESET)
        return

    # Deduct money and increment game turn
    game.money -= money_needed

    # Update infected population
    if infected_changing != 0:
        game.infected_population += infected_changing
        print(f"Infected population changed by {infected_changing}. Now it is {game.infected_population}" )
        time.sleep(1)

    if infection_rate != 0:
        game.infection_rate += infection_rate
        if infection_rate > 0:
            print(Colours.RED + f"The infection is spreading at an increased rate" + Colours.RESET)
        else:
            print(Colours.GREEN + f"The infection is spreading at an decreased rate" + Colours.RESET)
        time.sleep(1)

    # Update public dissatisfaction
    if dissatisfaction_changing != 0:
        game.public_dissatisfaction += dissatisfaction_changing
        print((Colours.RED if dissatisfaction_changing > 0 else Colours.GREEN) + f"Public dissatisfaction changed by {dissatisfaction_changing}. Now it is {game.public_dissatisfaction}" + Colours.RESET);
        time.sleep(1)

    # Update research progress
    if research_progress_changing != 0:
        game.research_progress += research_progress_changing
        print((Colours.BLUE if research_progress_changing > 0 else Colours.RED) + f"Research progress changed by {research_progress_changing}. Now it is {game.research_progress}" + Colours.RESET)
        time.sleep(1)

    # Execute any additional SQL query provided by the choice
    if sql_query:
        game_id = game.id  # Use the game object's id directly
        string_query = f"UPDATE airport_info {sql_query} WHERE game_id = {game_id}"
        db.run(string_query)

    # Display the choice text
    if text:
        print(text)


    # Record the choice in the database (after processing the choice)
    choice_id = db.run(f"SELECT id FROM choices WHERE name = '{name}'")[0][0]
    db.run(f"INSERT INTO choices_made (game_id, choice_id) VALUES ({game.id}, {choice_id});")


def get_airport_coordinates(icao_code):
    try:
        connection = mysql.connector.connect(
            user="yehort",
            password="root123",
            host="mysql.metropolia.fi",
            port=3306,
            database="yehort"
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

#def outbreak_notification(game)