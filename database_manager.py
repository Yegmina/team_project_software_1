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


#Each game' database should consist of 30 airports
#Below is the table specifying which contients should have how many airports
#AF - 7 ; AS - 7 ; EU - 6
#NA - 5 ; OC - 3 ; SA & AN - 1

#<editor-fold desc="Database manager v1.0">

## Formatting each player's game's name into one without spaces
def format_name(s) :
    s = list(s)
    for i in range(len(s)) :
        if s[i] == ' ' : s[i] = '_'
        else: s[i] = s[i].lower()
    return 'game_' + "".join(s)


def saved_games_database() :
    run(f"CREATE TABLE IF NOT EXISTS `saved_games` ("                               ##The table saves all
        f"  `id`                     INT(16) PRIMARY KEY AUTO_INCREMENT,"       ##of each game's variables
        f"  `input_name`             VARCHAR(64),"
        f"  `money`                  INT(16),"                                      ##It also saves the
        f"  `infected_population`    INT(16),"                                      ##name in formatted version
        f"  `public_dissatisfaction` INT(16),"                                      ##and the original (user input)
        f"  `research_progress`      INT(16),"                                      ##version.
        f"  `game_over`              BOOLEAN DEFAULT FALSE,"
        f"  `game_turn`              INT(16)"
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    #
    run(f"CREATE TABLE IF NOT EXISTS `airport_info` ("
        f"  `game_id`                INT(16),"
        f"  `airport_id`             VARCHAR(40) NOT NULL,"
        f"  `infected`               BOOLEAN DEFAULT FALSE,"
        f"  `closed`                 BOOLEAN DEFAULT FALSE,"
        f"  FOREIGN KEY (airport_id)"
        f"           REFERENCES airport(ident),"
        f"  FOREIGN KEY (game_id)"
        f"           REFERENCES saved_games(id)"
        f") ENGINE=InnoDB DEFAULT CHARSET=latin1;")