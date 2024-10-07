### Noah's Code Goes Here ###
'''
i = 0
growthrate = 2
local_infected_population = 1
while i < 50 and local_infected_population < 100:
    local_infected_population = int(local_infected_population * growthrate)
    print(local_infected_population)
    i += 1
import database_manager as db
infected_poplulation = 1
infection_multiplyer = 2
def infection_spread(local_infected_population, )
    infected_population*infection_multiplyer
    print(inefcted_population)
    '''
from random import randint

import Yehor
import database_manager as db

def infection_spread(game_name,infection_rate):
    infected_airport_list = db.run(f"SELECT airport_id FROM saved_games "
                                    f"RIGHT OUTER JOIN airport_info on airport_info.game_id = saved_games.id "
                                    f"WHERE input_name = '{game_name}' "
                                    f"AND infected = 1 "
                                    f"AND closed = 0;")
    for i in infected_airport_list:
        airport_spread(infected_airport_list[i],game_name,infection_rate)


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

#
def close_1_airport(icao_code):
    db.run(f'UPDATE airport_info'
           f'SET closed = {True}'
           f'WHERE airport_id = {icao_code};')

def close_continents_airports(continent):
    db.run(f'select airport_id from airport_info,airport where continent = {continent} and airport_id = ident;')
