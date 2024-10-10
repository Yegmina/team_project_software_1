### Noah's Code Goes Here ###
from random import randint

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

def print_all_icao_codes(game_id, highlighted_continent):

    icao_code_list = db.run(f'SELECT airport_id, infected, closed, continent FROM airport_info '
                            f'LEFT JOIN airport ON airport.ident = airport_id '
                            f'WHERE game_id = "{game_id}";')

    for i in range(len(icao_code_list)) :
        airport_info = f"{icao_code_list[i][0]} : {icao_code_list[i][3]}"
        condition = (icao_code_list[i][3] == highlighted_continent
                     and not icao_code_list[i][1] == 1
                     and not icao_code_list[i][2] == 1)
        output_string = (f"{(Colours.RED if icao_code_list[i][1] == 1 else Colours.GREEN)}"
                        f"{(Colours.STRIKE if icao_code_list[i][2] == 1 else '')}"
                        f"{(Colours.MAGENTA + Colours.BOLD if (condition == True) else '')}"
                        f"{f'{i + 1}.' : <3}{airport_info:^20}"
                        f"{Colours.RESET}")

        print(f"{output_string}", end = '' if i % 3 != 2 else '\n')

def check_and_close_airport(game_id, input_icao_code):

    icao_code_list = db.run(f'SELECT airport_id '
                            f'FROM airport_info '
                            f'WHERE game_id = "{game_id}";')

    if any(input_icao_code in icao_code[0] for icao_code in icao_code_list):
        close_1_airport(game_id, input_icao_code)
        print(f"Airport {input_icao_code} has been closed.")
        return True
    else:
        print('Not a proper input. Please enter "Done" or an ICAO code listed above.')
        return False


def close_1_airport(game_id, icao_code):
    db.run(f'UPDATE airport_info '
           f'SET closed = 1 '
           f'WHERE airport_id = "{icao_code}" '
           f'AND game_id = "{game_id}";')

def close_continents_airports(game_id, continent):
    airports = db.run(f"SELECT airport_id FROM airport_info "
                      f"LEFT JOIN airport ON airport.ident = airport_id "
                      f"WHERE airport.continent = '{continent}' "
                      f"AND airport_info.game_id = {game_id};")
    if len(airports) == 0 :
        print('Not a proper input. Please enter "Done" or a Continent code listed above.')
        return False
    else :
        print_all_icao_codes(game_id, continent)
        player_choice = input("Are you sure you want to close these airports (Highlighted in Purple)\n"
                              "YES (1) or NO (2):")
        while True :
            if player_choice == '1' :
                count = db.run(f"SELECT COUNT(*) FROM airport_info "
                               f"LEFT JOIN airport ON airport.ident = airport_id "
                               f"WHERE continent = '{continent}' "
                               f"AND infected = 0 "
                               f"AND closed = 0 "
                               f"AND game_id = {game_id};")[0][0]

                for airport in airports :
                    db.run(f"UPDATE airport_info "
                           f"SET closed = 1 "
                           f"WHERE airport_id = '{airport[0]}' "
                           f"AND game_id = {game_id}")
                print(f"{count} airports have been closed.")
                return True
            elif player_choice == '2' :
                return False

            else :
                print("Please enter 1 or 2.")
                continue

# print_all_icao_codes(86, 'EU')