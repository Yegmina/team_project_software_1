import mariadb
from geopy.distance import geodesic
import json
import database_initializing as db
import main

def load_choices_from_json(local_json_file):
    with open(local_json_file, 'r') as file:
        data = json.load(file)
        return data['choices']  # Returns the list of choices


def convert_choice_to_tuple(local_choice_dict):
    return (
        local_choice_dict['local_name'],
        local_choice_dict['local_money_needed'],
        local_choice_dict['local_infected_changing'],
        local_choice_dict['local_dissatisfaction_changing'],
        local_choice_dict['local_research_progress_changing'],
        local_choice_dict['local_text'],
        local_choice_dict['local_sql_query']
    )


def function():
    print("Hello")
    return


def payment_choice(game, local_choice_tuple):
    local_name, local_money_needed, local_infected_changing, local_dissatisfaction_changing, local_research_progress_changing, local_text, local_sql_query = local_choice_tuple

    if local_money_needed > game.money:
        print("Not enough money to do this choice.")
    else:
        game.money -= local_money_needed
        game.game_turn += 1
        game.infected_population += local_infected_changing
        game.public_dissatisfaction += local_dissatisfaction_changing
        game.research_progress += local_research_progress_changing
        if local_sql_query!="":
            local_string_query=f"UPDATE {game.designated_db_table}\n {local_sql_query}"
            db.run(local_string_query)
        # print(f"UPDATE {game.designated_db_table}\n SET closed = 1\n WHERE 1=1")
        #print(game.designated_db_table)


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



def distance_between_two(local_coordinates_1, local_coordinates_2):
    if local_coordinates_1 and local_coordinates_2:
        distance = geodesic(local_coordinates_1, local_coordinates_2).kilometers
        return distance
    else:
        return 999999999 # can be changed
