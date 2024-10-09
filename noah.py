### Noah's Code Goes Here ###
from random import randint

import Colours
import Yehor
import database_manager as db
import Colours

def infection_spread(game_name,infection_rate):
    infected_airport_list = db.run(f"SELECT airport_id FROM saved_games "
                                    f"RIGHT OUTER JOIN airport_info on airport_info.game_id = saved_games.id "
                                    f"WHERE input_name = '{game_name}' "
                                    f"AND infected = 1 "
                                    f"AND closed = 0;")
    for i in range(infected_airport_list):
        airport_spread(infected_airport_list[i][0],game_name,infection_rate)


# Checks if another country will get infected through a flight.
def airport_spread(spreading_airport,game_name,infection_rate):

    game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{game_name}';")[0][0]
    ##How far planes fly
    plane_flight_distance = 2000

    #Checks to see if the airport is infected and thus able to infect other countries
    if db.run(f"SELECT infected FROM airport_info WHERE game_id = '{game_id}' and airport_id = '{spreading_airport}';")[0][0]:
        spreading_airport = Yehor.get_airport_coordinates(spreading_airport)

        #Runs through all the airports in the current game and applys the infection chance
        table = db.run(f"SELECT airport_id FROM airport_info WHERE game_id = '{game_id}';")
        for country1 in table:
            airport1 = Yehor.get_airport_coordinates(country1[1])

            if Yehor.distance_between_two(spreading_airport,airport1) < plane_flight_distance and randint(0,100) < infection_rate:
                db.run(f'UPDATE airport_info '
                        f'SET infected = True '
                        f'WHERE airport_id = {country1[1]};')
    else:
        return

def print_all_icao_codes(game_name):
    game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{game_name}';")[0][0]

    icao_code_list = db.run(f'SELECT airport_id, infected, closed '
                            f'FROM airport_info '
                            f'WHERE game_id = "{game_id}";')

    for i in range(0, int(len(icao_code_list) / 3)):
        print(
            f"{(Colours.RED if icao_code_list[i][1] == 1 else Colours.GREEN)}"
            f"{(Colours.STRIKE if icao_code_list[i][2] == 1 else '')}"  # Strikethrough for closed airports
            f"{i + 1}. {icao_code_list[i][0]} "
            f"{Colours.RESET}"  # Reset after each section

            f"{(Colours.RED if icao_code_list[i + int(len(icao_code_list) / 3)][1] == 1 else Colours.GREEN)}"
            f"{(Colours.STRIKE if icao_code_list[i + int(len(icao_code_list) / 3)][2] == 1 else '')}"
            f"{i + int(len(icao_code_list) / 3) + 1}. {icao_code_list[i + int(len(icao_code_list) / 3)][0]} "
            f"{Colours.RESET}"

            f"{(Colours.RED if icao_code_list[i + int(len(icao_code_list) / 3) * 2][1] == 1 else Colours.GREEN)}"
            f"{(Colours.STRIKE if icao_code_list[i + int(len(icao_code_list) / 3) * 2][2] == 1 else '')}"
            f"{i + int(len(icao_code_list) / 3) * 2 + 1}. {icao_code_list[i + int(len(icao_code_list) / 3) * 2][0]} "
            f"{Colours.RESET}"
        )


def check_and_close_airport(game_name, input_icao_code):

    game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{game_name}';")[0][0]

    icao_code_list = db.run(f'SELECT airport_id '
                            f'FROM airport_info '
                            f'WHERE game_id = "{game_id}";')

    if any(input_icao_code in icao_code[0] for icao_code in icao_code_list):
        close_1_airport(input_icao_code)
        return True
    else:
        print('Not a proper ICAO code, try another')
        return False


def close_1_airport(icao_code):
    db.run(f'UPDATE airport_info '
           f'SET closed = 1 '
           f'WHERE airport_id = "{icao_code}";')

def close_continents_airports(continent):
    db.run(f'select airport_id from airport_info,airport where continent = {continent} and airport_id = ident;')