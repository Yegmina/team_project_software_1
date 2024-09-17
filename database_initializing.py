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

#Formatting each player's game's name into one without spaces
def remove_spacing(s) :
    s = list(s)
    for i in range(len(s)) :
        if s[i] == ' ' : s[i] = '_'
    return "".join(s)

#<editor-fold desc="IMPLEMENTATION OF INSERTING DATA INTO game_database DB">
def saved_games_database() :
    run(f"CREATE TABLE IF NOT EXISTS saved_games ("
        f"  name VARCHAR(10) NOT NULL,"
        f"  id INT PRIMARY KEY AUTO_INCREMENT"
        f")")

#ICAO Code - Infected (Bool) - Closed (Bool) - Large airport
def create_game_database(name) :
    name = remove_spacing(name)
    GameAirports = []

    continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
    NoCountriesEachContinent = (7, 7, 7, 5, 3, 1)
    for i in range(6) :
        query = (f"SELECT ident FROM airport "
                 f"WHERE continent = '{continents[i]}' "
                 f"AND type = 'large_airport';")
        customList = run(query)
        ##Holds all LARGE AIRPORTS from EACH continent

        for num in range(NoCountriesEachContinent[i]) :
            airport = customList[random.randint(0, len(customList) - 1)][0]
            if airport not in GameAirports:
                GameAirports.append(airport)            ##Randomizes from each continent the number of
                                                        ##necessary airports


    run(f"DROP TABLE IF EXISTS game_{name}")      ##Creating the table
    run(f"CREATE TABLE game_{name} ("
        f"  icao_code VARCHAR(10) NOT NULL,"            ##Airplane ICAO Code
        f"  infected BOOLEAN DEFAULT FALSE,"            ##Default Infected var is FALSE (Not infected)
        f"  closed BOOLEAN DEFAULT FALSE,"              ##Default Airport status var is FALSE (Not closed)
        f"  CONSTRAINT game_{name}_ibfk_1 FOREIGN KEY (icao_code) REFERENCES airport(ident)"      
            ##ICAO Code is directly connected to airport(ident)
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")

    for airport in GameAirports :
        run(f"INSERT INTO game_{name} VALUES ('{airport}', 0 , 0)")
#</editor-fold>


saved_games_database()