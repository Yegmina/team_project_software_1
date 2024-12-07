# utils/functions.py

"""DB basic functions"""
import mysql.connector
import mysql
import random

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
    """Creates a new game with the given name and sets up airport data."""
    # Check if the name is provided
    if not name:
        return {"error": "Name cannot be empty!"}, 400

    # Check if the game name already exists
    name_list = run(f"SELECT * FROM saved_games WHERE input_name = '{name}';")
    if name_list:
        return {"error": "Profile already exists!"}, 400

    # Insert the new game into the `saved_games` table
    run(f"""
        INSERT INTO saved_games (input_name, money, infected_population, 
                                  public_dissatisfaction, research_progress, 
                                  game_turn, infection_rate, max_distance) 
        VALUES ('{name}', 10000, 3, 7, 1, 1, 7, 8000); 
    """)

    # Fetch the newly created game ID
    game_id = run(f"SELECT id FROM saved_games WHERE input_name = '{name}';")[0][0]

    # Continent configuration: continents and the number of airports to select from each
    continents = ('AF', 'AS', 'EU', 'NA', 'OC', 'SA')
    countries_each_con = (7, 10, 5, 3, 1, 4)  # Number of airports to select per continent

    game_airports = []  # To store selected airport identifiers
    game_airports_countries = []  # To store selected countries

    for index, continent in enumerate(continents):
        # Fetch large airports in the current continent
        airports = run(f"""
            SELECT ident, iso_country FROM airport
            WHERE type = 'large_airport' AND continent = '{continent}';
        """)

        # Randomly select airports based on the required count for the continent
        for _ in range(countries_each_con[index]):
            rand_index = random.randint(0, len(airports) - 1)
            while (airports[rand_index][0] in game_airports or
                   airports[rand_index][1] in game_airports_countries):
                rand_index = random.randint(0, len(airports) - 1)

            # Add selected airport and its country to the lists
            game_airports.append(airports[rand_index][0])
            game_airports_countries.append(airports[rand_index][1])

    # Insert selected airports into the `airport_info` table for the current game
    for airport in game_airports:
        run(f"""
            INSERT INTO airport_info (game_id, airport_id, infected, closed)
            VALUES ({game_id}, '{airport}', 0, 0);
        """)

    # Randomly select one airport to be initially infected
    first_infected_airport = random.randint(0, len(game_airports) - 1)
    run(f"""
        UPDATE airport_info
        SET infected = 1
        WHERE game_id = {game_id} AND airport_id = '{game_airports[first_infected_airport]}';
    """)

    # Return a success message
    return {"message": "New game created successfully!", "game_name": name, "game_id": game_id}, 201


def get_all_games():
    """Fetches all saved games."""
    return run("SELECT * FROM saved_games")


def fetch_game(game_id):
    """Fetches a specific game by ID."""
    try:
        # Debugging: Log the game_id being fetched
        print(f"Fetching game with ID: {game_id}")

        # Execute the query with explicit column selection
        query = f"""
            SELECT 
                id, 
                input_name, 
                money, 
                infected_population, 
                public_dissatisfaction, 
                research_progress, 
                game_turn, 
                infection_rate, 
                max_distance 
            FROM saved_games 
            WHERE id = {game_id};
        """
        game_data = run(query)

        if not game_data:
            print(f"No game found with ID: {game_id}")  # Debugging
            return {"error": "Game not found!"}, 404

        # Debugging: Log the fetched data
        print(f"Fetched data: {game_data}")

        # Return the parsed game data
        return {
            "id": game_data[0][0],
            "name": game_data[0][1],
            "money": game_data[0][2],
            "infected_population": game_data[0][3],
            "public_dissatisfaction": game_data[0][4],
            "research_progress": game_data[0][5],
            "game_turn": game_data[0][6],  # Ensure correct field
            "infection_rate": game_data[0][7],
            "max_distance": game_data[0][8],
        }, 200
    except Exception as e:
        # Log and handle any exceptions
        print(f"Error fetching game: {e}")
        return {"error": str(e)}, 500


def fetch_games_by_name(input_name):
    """Fetches games with a matching name."""
    query = f"SELECT * FROM saved_games WHERE LOWER(input_name) = LOWER('{input_name}');"
    games = run(query)
    return [{"id": g[0], "input_name": g[1], "money": g[2], "infected_population": g[3],
             "public_dissatisfaction": g[4], "research_progress": g[5], "game_turn": g[6],
             "infection_rate": g[7], "max_distance": g[8]} for g in games]


def game_exists(game_name):
    """Checks if a game with the given name exists."""
    return run(f"SELECT * FROM saved_games WHERE input_name = '{game_name}';")


def check_and_update_game_status(game_id):
    """Checks game status and updates 'game_over' in the database if needed."""
    query = f"SELECT infected_population, public_dissatisfaction, research_progress FROM saved_games WHERE id = {game_id};"
    game = run(query)
    if not game:
        return {"error": "Game not found"}, False

    infected_population, public_dissatisfaction, research_progress = game[0]
    game_over = False
    message = None

    if infected_population >= 99:
        message = "The infection has spread globally. Game Over!"
        game_over = True
    elif infected_population <= 0:
        message = "Everyone is healed. Congratulations!"
        game_over = True
    elif public_dissatisfaction >= 100:
        message = "Public dissatisfaction has reached critical levels. Anarchy ensues. Game Over!"
        game_over = True
    elif research_progress >= 100:
        message = "The cure has been developed! You saved the world!"
        game_over = True

    if game_over:
        # Update the 'game_over' flag in the database
        update_query = f"UPDATE saved_games SET game_over = TRUE WHERE id = {game_id};"
        run(update_query)

    return {"message": message, "game_over": game_over}, game_over


def load_choices_from_db():
    """Loads all choices from the database."""
    query = """
        SELECT 
            id, 
            name, 
            money_needed AS cost, 
            infected_changing, 
            infection_rate, 
            dissatisfaction_changing, 
            research_progress_changing, 
            text 
        FROM choices;
    """
    # Make sure it returns a list of tuples
    return run(query)


def get_game_choices(game_id):
    """Fetches choices already made for a specific game."""
    query = f"SELECT choice_id FROM choices_made WHERE game_id = {game_id};"
    return [row[0] for row in run(query)]

def get_available_choices(game_id):
    """
    Returns choices that the player can make, excluding those already made.
    """
    # Fetch all choices
    all_choices = load_choices_from_db()

    # Get choices already made
    made_query = f"SELECT choice_id FROM choices_made WHERE game_id = {game_id};"
    made_choices = run(made_query)

    # Adjust for tuples instead of dictionaries
    made_choice_ids = {row[0] for row in made_choices}  # Assume `choice_id` is the first column

    # Filter available choices
    available_choices = [choice for choice in all_choices if choice[0] not in made_choice_ids]

    # Return as list of dictionaries for easier JSON serialization
    return [{"id": choice[0], "name": choice[1], "cost": choice[2]} for choice in available_choices]


def save_user_choice(game_id, choice_id):
    """Saves a user's choice to the database."""
    query = f"INSERT INTO choices_made (game_id, choice_id) VALUES ({game_id}, {choice_id});"
    run(query)


def payment_choice(game_id, choice_id):
    """
    Processes a player's choice by updating the game state in the database based on the selected choice.

    Args:
        game_id (int): The ID of the current game.
        choice_id (int): The ID of the selected choice.

    Returns:
        dict: JSON response indicating success or failure and any relevant messages.
    """
    # Retrieve choice details from the database
    choice_query = (
        f"SELECT money_needed, infected_changing, infection_rate, dissatisfaction_changing, "
        f"research_progress_changing, text, sql_query "
        f"FROM choices WHERE id = {choice_id};"
    )
    choice = run(choice_query)

    if not choice:
        return {"success": False, "message": "Invalid choice ID."}

    money_needed, infected_changing, infection_rate, dissatisfaction_changing, \
    research_progress_changing, text, sql_query = choice[0]

    # Check if the choice has already been made
    check_query = f"SELECT 1 FROM choices_made WHERE game_id = {game_id} AND choice_id = {choice_id};"
    already_made = run(check_query)

    if already_made:
        return {"success": False, "message": "Choice has already been made."}

    # Retrieve current game state
    game_query = (
        f"SELECT money, infected_population, public_dissatisfaction, research_progress, infection_rate "
        f"FROM saved_games WHERE id = {game_id};"
    )
    game_state = run(game_query)

    if not game_state:
        return {"success": False, "message": "Game not found."}

    money, infected_population, public_dissatisfaction, research_progress, current_infection_rate = game_state[0]

    # Check if the player can afford the choice
    if money_needed > money:
        return {"success": False, "message": "Not enough money to make this choice."}

    # Update game state variables
    updated_money = money - money_needed
    updated_infected_population = infected_population + (infected_changing or 0)
    updated_infection_rate = current_infection_rate + (infection_rate or 0)
    updated_public_dissatisfaction = max(0, min(100, public_dissatisfaction + (dissatisfaction_changing or 0)))
    updated_research_progress = max(0, min(100, research_progress + (research_progress_changing or 0)))

    # Update game state in the database
    update_game_query = (
        f"UPDATE saved_games "
        f"SET money = {updated_money}, infected_population = {updated_infected_population}, "
        f"public_dissatisfaction = {updated_public_dissatisfaction}, "
        f"research_progress = {updated_research_progress}, infection_rate = {updated_infection_rate} "
        f"WHERE id = {game_id};"
    )
    run(update_game_query)

    # Execute additional SQL query if provided
    if sql_query:
        update_airport_query = f"UPDATE airport_info {sql_query} WHERE game_id = {game_id};"
        run(update_airport_query)

    # Record the choice in the database
    record_choice_query = f"INSERT INTO choices_made (game_id, choice_id) VALUES ({game_id}, {choice_id});"
    run(record_choice_query)

    return {"success": True, "message": text or "Choice executed successfully."}

"""
def close_airport_by_icao(game_id, icao_code):
    run(f"UPDATE airport_info SET closed = 1 WHERE game_id = {game_id} AND airport_id = '{icao_code}';")
"""
"""test below"""





