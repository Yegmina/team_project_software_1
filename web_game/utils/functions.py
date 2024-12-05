# utils/functions.py

"""DB basic functions"""
import mysql.connector
import mysql

#<editor-fold desc = "MYSQL-cursor optimization">
connection = mysql.connector.connect(
    user="yehort",
    password="root123",
    host="mysql.metropolia.fi",
    port=3306,
    database="yehort",
    autocommit = True
)

cursor = connection.cursor()
def run(s) :
    cursor.execute(s)
    try :
        return cursor.fetchall()
    except mysql.connector.errors.InterfaceError as e :
        return e
    except Exception as e :
        return e


"""Game_creating, saving, retrieving list of games etc"""

def saved_games_database():
    """Initializes the saved games database."""
    """NOT IN USE RIGHT NOW!!!"""
    run(f"""
        CREATE TABLE IF NOT EXISTS `saved_games` (
            `id`                     INT(16) PRIMARY KEY AUTO_INCREMENT,
            `input_name`             VARCHAR(64),
            `money`                  INT(16),
            `infected_population`    INT(16),
            `public_dissatisfaction` INT(16),
            `research_progress`      INT(16),
            `game_over`              BOOLEAN DEFAULT FALSE,
            `game_turn`              INT(16),
            `infection_rate`         SMALLINT(5),
            `max_distance`           INT(16)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """)


def new_game(name):
    """Creates a new game with the given name."""
    name_list = run(f"SELECT * FROM saved_games WHERE input_name = '{name}';")
    if not name:
        return {"error": "Name cannot be empty!"}, 400

    if name_list:
        return {"error": "Profile already exists!"}, 400

    run(f"""
        INSERT INTO saved_games (input_name, money, infected_population, 
                                  public_dissatisfaction, research_progress, 
                                  game_turn, infection_rate, max_distance) 
        VALUES ('{name}', 10000, 3, 7, 0, 1, 7, 8000);
    """)
    return {"message": "New game created successfully!", "game_name": name}, 201


def get_all_games():
    """Fetches all saved games."""
    return run("SELECT * FROM saved_games")


def fetch_game(game_id):
    """Fetches a specific game by ID."""
    game_data = run(f"SELECT * FROM saved_games WHERE id = {game_id};")
    if not game_data:
        return {"error": "Game not found!"}, 404

    return {
        "id": game_data[0][0],
        "name": game_data[0][1],
        "money": game_data[0][2],
        "infected_population": game_data[0][3],
        "public_dissatisfaction": game_data[0][4],
        "research_progress": game_data[0][5],
        "game_turn": game_data[0][6],
        "infection_rate": game_data[0][7],
        "max_distance": game_data[0][8],
    }, 200


def game_exists(game_name):
    """Checks if a game with the given name exists."""
    return run(f"SELECT * FROM saved_games WHERE input_name = '{game_name}';")
