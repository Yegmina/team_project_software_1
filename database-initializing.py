import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database = 'flight_game',
    password = 'root',
    autocommit = True,
    collation = 'utf8mb4_general_ci',
)

#<editor-fold desc = "MYSQL-cursor optimization">
cursor = connection.cursor()

def run(s) :
    cursor.execute(s)
    try :
        return cursor.fetchall()
    except : pass
#</editor-fold>

#<editor-fold desc = "DATABASE CREATION">
        ###------ DATABASE CREATION ------###
try :
    cursor.execute(f"CREATE DATABASE game_database;")
    print(f'{"CREATING FILES":_^50}')
    print(f"{'Successfully created neccessary game files' :-^50}")

except :
    print(f"{'Files have been created' :-^50}")
        ###-------------------------------###
#</editor-fold>

#Each game' database should consist of 30 airports
#Below is the table specifying which contients should have how many airports
#AF - 7 ; AS - 7 ; EU - 6
#NA - 5 ; OC - 3 ; SA & AN - 1
#<editor-fold desc="IMPLEMENTATION OF THE GAME DATABASE CREATION">
import random
def create_game_database() :
    continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA', 'AN')
    NoCountriesEachContinent = (7, 7, 6, 5, 3, 1, 1)
    GameAirports = []

    for i in range(7) :
        query = f"SELECT name FROM airport WHERE continent = '{continents[i]}'"
        customList = run(query)

        for num in range(NoCountriesEachContinent[i]) :
            airport = customList[random.randint(0, len(customList) - 1)][0]
            if airport not in GameAirports:
                GameAirports.append(airport)

    ##I

    cursor.execute(f"USE game_database;")
#</editor-fold>