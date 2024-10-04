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

# Checks if another country will get infected through a flight.
def airport_spread(spreading_country):

    ##How far planes fly
    plane_flight_distance = 2000

    #Checks to see if the airport is infected and thus able to infect other countries
    if db.run(f"SELECT airport_id FROM airport_info WHERE game_id = {spreading_country};") == True:
        Yehor.get_airport_coordinates(spreading_country)

        #Runs through all the airports in the current game and applys the infection chance
        i = 1
        while i <= 30:
            country2 = db.run(f'SELECT airport_id FROM airport_info WHERE game_id = {i};')
            if Yehor.distance_between_two(spreading_country,country2) < plane_flight_distance:
                if randint(1,2) == 1:
                    db.run(f'UPDATE airport_info'
                    f'SET infected = {True}'
                    f'WHERE airport_id = {country2};')
                else:
                    return
            i+=1
    else:
        return

#
def close_1_airport(icao_code):
    db.run(f'UPDATE airport_info'
           f'SET closed = {True}'
           f'WHERE airport_id = {icao_code};')

def close_continents_airports(continent):
    db.run(f'select airport_id from airport_info,airport where continent = {continent} and airport_id = {continent};')
