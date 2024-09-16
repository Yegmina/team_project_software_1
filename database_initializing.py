import mariadb
import random

connection = mariadb.connect(
    host = 'localhost',
    user = 'root',
    database = 'flight_game',
    password = 'root',
    autocommit = True,
)

#<editor-fold desc = "MYSQL-cursor optimization">
cursor = connection.cursor()

def run(s) :
    cursor.execute(s)
    try :
        return cursor.fetchall()
    except :
        return None
#</editor-fold>


#Each game' database should consist of 30 airports
#Below is the table specifying which contients should have how many airports
#AF - 7 ; AS - 7 ; EU - 6
#NA - 5 ; OC - 3 ; SA & AN - 1
#<editor-fold desc="IMPLEMENTATION OF INSERTING DATA INTO game_database DB">

#ICAO Code - Infected (Bool) - Closed (Bool) - Large airport

GameAirports = []
def create_game_database(game_count) :

    continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
    NoCountriesEachContinent = (7, 7, 7, 5, 3, 1)
    for i in range(6) :
        query = (f"SELECT ident FROM airport WHERE continent = '{continents[i]}'"
                 f" AND type = 'large_airport'")
        customList = run(query)

        for num in range(NoCountriesEachContinent[i]) :
            airport = customList[random.randint(0, len(customList) - 1)][0]
            if airport not in GameAirports:
                GameAirports.append(airport)

    run(f"DROP TABLE IF EXISTS game_{game_count}")
    run(f"CREATE TABLE game_{game_count} ("
        f"  icao_code VARCHAR(10) NOT NULL,"
        f"  infected BOOLEAN DEFAULT FALSE,"
        f"  closed BOOLEAN DEFAULT FALSE,"
        f"  CONSTRAINT game_{game_count}_ibfk_1 FOREIGN KEY (icao_code) REFERENCES airport(ident)"
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")

    for airport in GameAirports :
        run(f"INSERT INTO game_{game_count} VALUES ('{airport}', 0 , 0)")
#</editor-fold>

create_game_database(1)

