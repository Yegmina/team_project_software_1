# utils/functions.py

"""DB basic functions"""
import mysql.connector
import mysql
from utils.ai.gemini import GeminiModel

#<editor-fold desc = "MYSQL-cursor optimization">
connection = mysql.connector.connect(
    user="yehort",
    password="root123",
    host="mysql.metropolia.fi",
    port=3306,
    database="yehort",
    autocommit = True,
    connection_timeout = 3,
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


import math
import random

def infection_spread(game_id, infection_rate):
    """
    Spreads infection from infected airports to nearby airports for the specified game.
    """
    try:
        # Fetch the list of currently infected and open airports for the game
        infected_airport_list = run(f"""
            SELECT airport_id 
            FROM airport_info
            WHERE game_id = {game_id} 
            AND infected = 1 
            AND closed = 0;
        """)

        if not infected_airport_list:
            return {"success": False, "message": "No infected airports available for spreading."}

        # Spread infection from each infected airport
        for airport in infected_airport_list:
            spreading_airport = airport[0]
            airport_spread(spreading_airport, game_id, infection_rate)

        return {"success": True, "message": f"Infection spread processed for game ID {game_id}."}

    except Exception as e:
        return {"success": False, "message": str(e)}


def airport_spread(spreading_airport, game_id, infection_rate):
    """
    Spreads infection from a single airport to nearby airports within flight range.
    """
    try:
        # Flight range in kilometers
        plane_flight_distance = 2000

        # Check if the airport is infected
        is_infected = run(f"""
            SELECT infected 
            FROM airport_info 
            WHERE game_id = {game_id} AND airport_id = '{spreading_airport}';
        """)[0][0]

        if not is_infected:
            return  # Skip if the airport is not infected

        # Get coordinates of the spreading airport
        spreading_airport_coords = get_airport_coordinates(spreading_airport)

        # Fetch all airports in the game
        airports_in_game = run(f"SELECT airport_id FROM airport_info WHERE game_id = {game_id};")

        # Spread infection to nearby airports
        for airport in airports_in_game:
            target_airport = airport[0]
            target_airport_coords = get_airport_coordinates(target_airport)

            # Calculate distance between airports
            distance = distance_between_two(spreading_airport_coords, target_airport_coords)

            # Spread infection based on distance and infection rate
            if distance < plane_flight_distance and random.randint(0, 100) < infection_rate:
                run(f"""
                    UPDATE airport_info 
                    SET infected = 1 
                    WHERE game_id = {game_id} AND airport_id = '{target_airport}';
                """)

    except Exception as e:
        print(f"Error in airport_spread: {e}")


def get_airport_coordinates(airport_id):
    """
    Fetches the latitude and longitude of an airport by its ID.
    """
    coords = run(f"""
        SELECT latitude_deg, longitude_deg 
        FROM airport 
        WHERE ident = '{airport_id}';
    """)
    if coords:
        return coords[0]
    return None


def distance_between_two(coord1, coord2):
    """
    Calculates the distance in kilometers between two sets of coordinates using the haversine formula.
    """
    if not coord1 or not coord2:
        return float('inf')  # Return infinity if coordinates are invalid

    # Unpack coordinates
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Earth in kilometers
    R = 6371
    return R * c

"""
def close_airport_by_icao(game_id, icao_code):
    run(f"UPDATE airport_info SET closed = 1 WHERE game_id = {game_id} AND airport_id = '{icao_code}';")
"""
"""test below"""

def get_random_events_examples():
    """Retrieve random events from examples.txt from random_events"""
    with open("./random_events/examples.txt", "r") as file:
        lines=file.readlines()

    return lines

def handle_random_event(game_id):
    """
    Handles the logic of generating and applying a random event using Gemini AI.
    """
    try:
        # Load Gemini model
        gemini_model = GeminiModel()

        # Random event prompt
        random_event_prompt = (
            "Generate details for a single random event in a strategy game where the player manages global variables "
            "like money, infected population, and public dissatisfaction. The event should include a title, a short "
            "description, and changes to the variables (Money: ±X, Infected: ±X, Dissatisfaction: ±X). Provide only one "
            "event per request. DO NOT provide any other information. Money is int from -1000 to 1000. Infected is int from -5 to 5, dissatisfaction is int from -5 to 5\n\n"
            "Your answer MUST have this structure:\n\n"
            "Title: {title}\n\n"
            "Description: {description}\n\n"
            "Money: {money}\n\n"
            "Infected: {infected}\n\n"
            "Dissatisfaction: {dissatisfaction}"
        )

        # Call Gemini model to generate the random event
        gemini_response = gemini_model.call_model(user_prompt=random_event_prompt)

        # Parse the Gemini response
        parsed_event = parse_gemini_response(gemini_response)

        # Fetch current game state
        game_query = f"SELECT money, infected_population, public_dissatisfaction FROM saved_games WHERE id = {game_id};"
        game_state = run(game_query)
        if not game_state:
            return {"success": False, "message": "Game not found."}

        # Update game state based on the event
        money, infected_population, public_dissatisfaction = game_state[0]
        updated_money = max(0, money + parsed_event["money"])
        updated_infected_population = max(0, infected_population + parsed_event["infected"])
        updated_public_dissatisfaction = max(0, min(100, public_dissatisfaction + parsed_event["dissatisfaction"]))

        # Save updated game state to the database
        update_query = f"""
            UPDATE saved_games
            SET money = {updated_money}, 
                infected_population = {updated_infected_population}, 
                public_dissatisfaction = {updated_public_dissatisfaction}
            WHERE id = {game_id};
        """
        run(update_query)

        # Return the parsed event and updated game state
        return {
            "success": True,
            "event": parsed_event,
            "updated_game_state": {
                "money": updated_money,
                "infected_population": updated_infected_population,
                "public_dissatisfaction": updated_public_dissatisfaction
            }
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


def parse_gemini_response(response):
    """
    Parses the response from Gemini into a structured dictionary.
    """
    lines = response.splitlines()
    parsed_event = {}

    for line in lines:
        if line.startswith("Title: "):
            parsed_event["title"] = line.replace("Title: ", "").strip()
        elif line.startswith("Description: "):
            parsed_event["description"] = line.replace("Description: ", "").strip()
        elif line.startswith("Money: "):
            parsed_event["money"] = int(line.replace("Money: ", "").strip())
        elif line.startswith("Infected: "):
            parsed_event["infected"] = int(line.replace("Infected: ", "").strip())
        elif line.startswith("Dissatisfaction: "):
            parsed_event["dissatisfaction"] = int(line.replace("Dissatisfaction: ", "").strip())

    return parsed_event


def handle_infection_spread(game_id):
    """
    Handles the infection spread logic by fetching the infection rate and spreading the infection.
    """
    try:
        # Fetch the infection rate for the game
        infection_rate_query = f"""
            SELECT infection_rate 
            FROM saved_games 
            WHERE id = {game_id};
        """
        infection_rate_result = run(infection_rate_query)

        if not infection_rate_result:
            return {"success": False, "message": f"Game ID {game_id} not found."}

        infection_rate = infection_rate_result[0][0]

        # Fetch a list of infected airports before the spread
        previously_infected_query = f"""
            SELECT airport_id
            FROM airport_info
            WHERE game_id = {game_id} AND infected = 1;
        """
        previously_infected = {row[0] for row in run(previously_infected_query)}

        # Track flight paths during the infection spread
        flight_paths = []
        infection_spread(game_id, infection_rate, flight_paths)

        # Fetch a list of all airports after the spread
        all_airports_query = f"""
            SELECT airport_id, infected, closed
            FROM airport_info
            WHERE game_id = {game_id};
        """
        all_airports = run(all_airports_query)

        # Identify newly infected airports
        newly_infected_query = f"""
            SELECT airport_id
            FROM airport_info
            WHERE game_id = {game_id} AND infected = 1;
        """
        newly_infected = {row[0] for row in run(newly_infected_query)} - previously_infected

        # Format the response
        response = {
            "success": True,
            "message": f"Infection spread processed for game ID {game_id}.",
            "newly_infected_airports": list(newly_infected),
            "flight_paths": flight_paths,
            "all_airports": [
                {
                    "airport_id": row[0],
                    "infected": bool(row[1]),
                    "closed": bool(row[2])
                }
                for row in all_airports
            ]
        }

        return response

    except Exception as e:
        return {"success": False, "message": str(e)}


def infection_spread(game_id, infection_rate, flight_paths):
    """
    Spreads infection from infected airports to nearby airports for the specified game.
    """
    try:
        # Fetch the list of currently infected and open airports for the game
        infected_airport_list = run(f"""
            SELECT airport_id 
            FROM airport_info
            WHERE game_id = {game_id} 
            AND infected = 1 
            AND closed = 0;
        """)

        if not infected_airport_list:
            return {"success": False, "message": "No infected airports available for spreading."}

        # Spread infection from each infected airport
        for airport in infected_airport_list:
            spreading_airport = airport[0]
            airport_spread(spreading_airport, game_id, infection_rate, flight_paths)

    except Exception as e:
        print(f"Error in infection_spread: {e}")


def airport_spread(spreading_airport, game_id, infection_rate, flight_paths):
    """
    Spreads infection from a single airport to nearby airports within flight range.
    Tracks flight paths contributing to the spread.
    """
    try:
        # Fetch max flight distance from the database
        max_distance_query = f"""
            SELECT max_distance
            FROM saved_games
            WHERE id = {game_id};
        """
        max_distance_result = run(max_distance_query)
        if not max_distance_result:
            raise ValueError(f"Max distance not found for game ID {game_id}.")
        max_distance = max_distance_result[0][0]

        # Check if the airport is infected
        is_infected = run(f"""
            SELECT infected 
            FROM airport_info 
            WHERE game_id = {game_id} AND airport_id = '{spreading_airport}';
        """)[0][0]

        if not is_infected:
            return  # Skip if the airport is not infected

        # Get coordinates of the spreading airport
        spreading_airport_coords = get_airport_coordinates(spreading_airport)

        # Fetch all airports in the game
        airports_in_game = run(f"SELECT airport_id FROM airport_info WHERE game_id = {game_id};")

        # Spread infection to nearby airports
        for airport in airports_in_game:
            target_airport = airport[0]
            target_airport_coords = get_airport_coordinates(target_airport)

            # Calculate distance between airports
            distance = distance_between_two(spreading_airport_coords, target_airport_coords)

            # Spread infection based on distance and infection rate
            if distance < max_distance and random.randint(0, 100) < infection_rate:
                # Update the target airport as infected
                run(f"""
                    UPDATE airport_info 
                    SET infected = 1 
                    WHERE game_id = {game_id} AND airport_id = '{target_airport}';
                """)

                # Record the flight path
                flight_paths.append({
                    "from": spreading_airport,
                    "to": target_airport,
                    "distance": distance
                })

    except Exception as e:
        print(f"Error in airport_spread: {e}")


