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
def format_name(s) :
    s = list(s)
    for i in range(len(s)) :
        if s[i] == ' ' : s[i] = '_'
        else: s[i] = s[i].lower()
    return 'game_' + "".join(s)


#<editor-fold desc="IMPLEMENTATION OF INSERTING DATA INTO game_database DB">
def saved_games_database() :
    run(f"CREATE TABLE IF NOT EXISTS `saved_games` ("               ##The table saves all
        f"  `name`                   VARCHAR(64) PRIMARY KEY,"      ##of each game's variables
        f"  `input_name`             VARCHAR(64),"                          
        f"  `money`                  INT(16),"                      ##It also saves the 
        f"  `infected_population`    INT(16),"                      ##name in formatted version
        f"  `public_dissatisfaction` INT(16),"                      ##and the original (user input)
        f"  `research_progress`      INT(16),"                      ##version.
        f"  `game_over`              BOOLEAN DEFAULT FALSE,"
        f"  `game_turn`              INT(16)"
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")


def create_game_database(name) :

    formatted_name = format_name(name)

    # ICAO Code - Infected (Bool) - Closed (Bool) - Large airport
    run(f"DROP TABLE IF EXISTS {formatted_name};")                  ##Creating the table
    run(f"CREATE TABLE {formatted_name} ("
        f"  icao_code           VARCHAR(10) NOT NULL,"              ##Airplane ICAO Code
        f"  infected            INT(16),"             ##Default Infected var is FALSE (Not infected)
        f"  closed              BOOLEAN DEFAULT FALSE,"             ##Default Airport status var is FALSE (Not closed)
        f"  CONSTRAINT {formatted_name}_ibfk_1 FOREIGN KEY (icao_code) REFERENCES airport(ident)"      
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")
            ##ICAO Code is directly connected to airport(ident)


    #Inserting the game's data into the saved_games (Holds all games) table
    #All values are initialized values (As copied from main.py)
    run(f"INSERT INTO saved_games VALUES "
        f"('{formatted_name}',"            ## Name
        f" '{name}',"                      ## User-input name                            
        f" 1000000,"                       ## Initial money
        f" 10,"                            ## Initial infected_population
        f" 10,"                            ## Initial public_dissatisfaction
        f" 0,"                             ## Initial research_progress
        f" False,"                         ## Initial game_over as False
        f" 1);")                           ## Initial game_turn as 0


    ##Generating random 'large airports' around the globe,
    ##Each continents have its due number of airports
    GameAirports = []

    continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
    NoCountriesEachContinent = (7, 7, 7, 5, 3, 1)
    for i in range(6) :
        query = (f"SELECT   ident FROM airport "
                 f"WHERE    continent = '{continents[i]}' "
                 f"AND      type = 'large_airport';")
        customList = run(query)
        ##Holds all LARGE AIRPORTS from EACH continent

        for num in range(NoCountriesEachContinent[i]) :
            airport = customList[random.randint(0, len(customList) - 1)][0]
            while airport in GameAirports:
                airport = customList[random.randint(0, len(customList) - 1)][0]
            GameAirports.append(airport)

                                                        ##necessary airports
    for airport in GameAirports :
        run(f"INSERT INTO {formatted_name} VALUES ('{airport}', 0 , 0)")


##The project needs another game-saving function (DATA FOR EACH GAME)
##And the 'Continue' option in Tai.py needs to fetch data for each saved games

#</editor-fold>
