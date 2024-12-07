import random

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from flask_cors import CORS
from utils.gemini import GeminiModel

from utils.functions import *  # Import all functions from functions.py
import json


app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Define the route for the home page, by home page launch index.html from templace folder
@app.route('/')
def index():
    """Home page showing game options."""
    games = get_all_games()
    return render_template('index.html', games=json.dumps(games))


@app.route('/new_game', methods=['GET', 'POST'])
def create_new_game():
    """Handles new game creation."""
    if request.method == 'POST':
        name = request.get_json()['name']
        response, status = new_game(name)
        game_id = fetch_games_by_name(response['game_name'])[0]['id']
        if status == 201:
            return redirect(url_for('play', game_id=game_id))
        return render_template('new_game.html', error=response['error'])

    return render_template('new_game.html')


@app.route('/fetch_game/<int:game_id>', methods=['GET'])
def get_game_details(game_id):
    """Fetches game details."""
    response, status = fetch_game(game_id)
    if status == 200:
        return render_template('game_details.html', game=json.dumps(response))
    return jsonify(response), status

## Dev-functions
@app.route('/dev/fetch_games/<int:id>', methods=['GET'])
def dev_fetch_game(id):
    data = fetch_game(id)
    return data

@app.route('/dev/game_exists/<game_name>')
def dev_game_exists(game_name):
    data = game_exists(game_name)
    return json.dumps(data)

@app.route('/play/<game_id>')
def play(game_id):
    data = fetch_game(game_id)
    return render_template('gameplay.html', game=json.dumps(data))


@app.route('/api/games/search', methods=['GET'])
def api_fetch_games_by_name():
    """API endpoint to search games by name."""
    input_name = request.args.get('name')
    if not input_name:
        return jsonify({"status": "error", "message": "Name parameter is required"}), 400
    games = fetch_games_by_name(input_name)
    if not games:
        return jsonify({"status": "error", "message": "No games found"}), 404
    return jsonify({"status": "success", "games": games}), 200


@app.route('/api/games/<int:game_id>/check_status', methods=['GET'])
def api_check_game_status(game_id):
    """API endpoint to check the game status and update 'game_over' if needed."""
    status, is_game_over = check_and_update_game_status(game_id)
    if "error" in status:
        return jsonify({"status": "error", "message": status["error"]}), 404

    return jsonify({"status": "success", "game_over": is_game_over, "message": status["message"]}), 200


@app.route('/api/games/<int:game_id>/make_choice', methods=['GET'])
def api_make_choice(game_id):
    try:
        available_choices = get_available_choices(game_id)
        return jsonify({"choices": available_choices, "success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/games/<int:game_id>/process_choice', methods=['POST'])
def api_process_choice(game_id):
    """
    Processes a player's choice by checking if it's valid, applying changes
    to the game state, and updating the database accordingly.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Content-Type must be application/json."}), 415

    data = request.json
    if not data:
        return jsonify({"success": False, "message": "Request body is required."}), 400

    choice_id = data.get("choice_id")
    if not choice_id:
        return jsonify({"success": False, "message": "Choice ID is required."}), 400

    already_made_query = f"SELECT 1 FROM choices_made WHERE game_id = {game_id} AND choice_id = {choice_id};"
    already_made = run(already_made_query)
    if already_made:
        return jsonify({"success": False, "message": "Choice has already been made."}), 400

    choice_query = (
        f"SELECT money_needed, infected_changing, infection_rate, dissatisfaction_changing, "
        f"research_progress_changing, text, sql_query "
        f"FROM choices WHERE id = {choice_id};"
    )
    choice = run(choice_query)
    if not choice:
        return jsonify({"success": False, "message": "Invalid choice ID."}), 404

    money_needed, infected_changing, infection_rate, dissatisfaction_changing, \
    research_progress_changing, text, sql_query = choice[0]

    game_query = (
        f"SELECT money, infected_population, public_dissatisfaction, research_progress, "
        f"infection_rate, game_turn, max_distance "
        f"FROM saved_games WHERE id = {game_id};"
    )
    game_state = run(game_query)
    if not game_state:
        return jsonify({"success": False, "message": "Game not found."}), 404

    money, infected_population, public_dissatisfaction, research_progress, \
    current_infection_rate, game_turn, max_distance = game_state[0]

    if money_needed > money:
        return jsonify({"success": False, "message": "Not enough money to make this choice."}), 400

    updated_money = money - money_needed
    updated_infected_population = max(0, infected_population + (infected_changing or 0))
    updated_infection_rate = current_infection_rate + (infection_rate or 0)
    updated_public_dissatisfaction = max(0, min(100, public_dissatisfaction + (dissatisfaction_changing or 0)))
    updated_research_progress = max(0, min(100, research_progress + (research_progress_changing or 0)))
    updated_game_turn = game_turn + 1 # IDK WHY BUT IT IS NOT UPGRADING SOMETIMES LOL
    updated_max_distance = max_distance + 10

    update_game_query = (
        f"UPDATE saved_games "
        f"SET money = {updated_money}, infected_population = {updated_infected_population}, "
        f"public_dissatisfaction = {updated_public_dissatisfaction}, "
        f"research_progress = {updated_research_progress}, infection_rate = {updated_infection_rate}, "
        f"game_turn = {updated_game_turn}, max_distance = {updated_max_distance} "
        f"WHERE id = {game_id};"
    )
    print("Executing Update Query:", update_game_query)  # Debugging
    run(update_game_query)

    if sql_query:
        run(f"UPDATE airport_info {sql_query} WHERE game_id = {game_id};")

    record_choice_query = f"INSERT INTO choices_made (game_id, choice_id) VALUES ({game_id}, {choice_id});"
    run(record_choice_query)

    return jsonify({
        "success": True,
        "message": text or "Choice executed successfully.",
        "updated_game_state": {
            "money": updated_money,
            "infected_population": updated_infected_population,
            "public_dissatisfaction": updated_public_dissatisfaction,
            "research_progress": updated_research_progress,
            "infection_rate": updated_infection_rate,
            "game_turn": updated_game_turn,
            "max_distance": updated_max_distance,
        }
    }), 200

@app.route('/api/airports/close', methods=['POST'])
def close_airport():
    """
    Closes an airport and updates the game's money and public dissatisfaction.
    Ensures the airport exists and is open before closing it.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Content-Type must be application/json."}), 415

    data = request.json
    game_id = data.get("game_id")
    airport_id = data.get("airport_id")
    money_cost = 5000  # Cost to close an airport
    dissatisfaction_increase = 10  # Public dissatisfaction increase for closing an airport

    if not game_id or not airport_id:
        return jsonify({"success": False, "message": "Game ID and Airport ID are required."}), 400

    try:
        # Check if the airport exists and is open
        airport_check_query = f"""
            SELECT closed FROM airport_info
            WHERE game_id = {game_id} AND airport_id = '{airport_id}';
        """
        airport_state = run(airport_check_query)
        if not airport_state:
            return jsonify({"success": False, "message": f"Airport {airport_id} not found for game ID {game_id}."}), 404

        is_closed = airport_state[0][0]
        if is_closed:
            return jsonify({"success": False, "message": f"Airport {airport_id} is already closed."}), 400

        # Fetch current game state
        game_query = f"SELECT money, public_dissatisfaction FROM saved_games WHERE id = {game_id};"
        game_state = run(game_query)
        if not game_state:
            return jsonify({"success": False, "message": "Game not found."}), 404

        money, public_dissatisfaction = game_state[0]

        # Check if the player can afford to close the airport
        if money < money_cost:
            return jsonify({"success": False, "message": "Not enough money to close the airport."}), 400

        # Update airport status to closed
        update_airport_query = f"""
            UPDATE airport_info
            SET closed = 1
            WHERE game_id = {game_id} AND airport_id = '{airport_id}';
        """
        run(update_airport_query)

        # Verify the airport is now closed
        verify_closure_query = f"""
            SELECT closed FROM airport_info
            WHERE game_id = {game_id} AND airport_id = '{airport_id}';
        """
        updated_state = run(verify_closure_query)
        if not updated_state or updated_state[0][0] != 1:
            return jsonify({"success": False, "message": f"Failed to close airport {airport_id}."}), 500

        # Update game state
        updated_money = money - money_cost
        updated_dissatisfaction = min(100, public_dissatisfaction + dissatisfaction_increase)
        update_game_query = f"""
            UPDATE saved_games
            SET money = {updated_money}, public_dissatisfaction = {updated_dissatisfaction}
            WHERE id = {game_id};
        """
        run(update_game_query)

        return jsonify({
            "success": True,
            "message": f"Airport {airport_id} has been successfully closed.",
            "airport_state": {
                "game_id": game_id,
                "airport_id": airport_id,
                "closed": True
            },
            "updated_game_state": {
                "money": updated_money,
                "public_dissatisfaction": updated_dissatisfaction,
            },
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.route('/api/airports/<int:game_id>', methods=['GET'])
def get_all_airports(game_id):
    """
    Fetches a list of all airports for a specific game ID with their statuses and related information.
    """
    query = f"""
        SELECT a.game_id, a.airport_id, a.infected, a.closed, g.money, g.public_dissatisfaction
        FROM airport_info AS a
        JOIN saved_games AS g ON a.game_id = g.id
        WHERE a.game_id = {game_id};
    """
    try:
        airports = run(query)
        if not airports:
            return jsonify({"success": False, "message": f"No airports found for game_id {game_id}."}), 404

        result = [
            {
                "game_id": row[0],
                "airport_id": row[1],
                "infected": bool(row[2]),
                "closed": bool(row[3]),
                "money": row[4],
                "public_dissatisfaction": row[5],
            }
            for row in airports
        ]
        return jsonify({"success": True, "airports": result}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.route('/api/airports/info/<string:airport_id>', methods=['GET'])
def get_all_info_one_airport(airport_id):
    """
    Fetches detailed information about an airport, including:
    - Data from the `airport` table
    - Data from the `airport_info` table for its involvement in games
    """
    try:
        # Fetch information from the `airport` table
        airport_query = f"""
            SELECT id, ident, type, name, latitude_deg, longitude_deg, elevation_ft,
                   continent, iso_country, iso_region, municipality, scheduled_service,
                   gps_code, iata_code, local_code, home_link, wikipedia_link, keywords
            FROM airport
            WHERE ident = '{airport_id}';
        """
        airport_data = run(airport_query)
        if not airport_data:
            return jsonify({"success": False, "message": f"Airport {airport_id} not found in airport table."}), 404

        # Unpack airport data
        airport_info = {
            "id": airport_data[0][0],
            "ident": airport_data[0][1],
            "type": airport_data[0][2],
            "name": airport_data[0][3],
            "latitude_deg": airport_data[0][4],
            "longitude_deg": airport_data[0][5],
            "elevation_ft": airport_data[0][6],
            "continent": airport_data[0][7],
            "iso_country": airport_data[0][8],
            "iso_region": airport_data[0][9],
            "municipality": airport_data[0][10],
            "scheduled_service": airport_data[0][11],
            "gps_code": airport_data[0][12],
            "iata_code": airport_data[0][13],
            "local_code": airport_data[0][14],
            "home_link": airport_data[0][15],
            "wikipedia_link": airport_data[0][16],
            "keywords": airport_data[0][17],
        }

        # Fetch game-related data from the `airport_info` table
        game_query = f"""
            SELECT game_id, infected, closed
            FROM airport_info
            WHERE airport_id = '{airport_id}';
        """
        game_data = run(game_query)
        if not game_data:
            return jsonify({"success": True, "airport": airport_info, "game_info": []}), 200

        # Format game-related data
        game_info = [
            {"game_id": row[0], "infected": bool(row[1]), "closed": bool(row[2])}
            for row in game_data
        ]

        # Combine both data sets into the response
        return jsonify({"success": True, "airport": airport_info, "game_info": game_info}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/airports/close_continent', methods=['POST'])
def close_continent_airports():
    """
    Closes all airports in a specific continent for a given game.
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Content-Type must be application/json."}), 415

    data = request.json
    game_id = data.get("game_id")
    continent = data.get("continent")

    if not game_id or not continent:
        return jsonify({"success": False, "message": "Game ID and Continent are required."}), 400

    try:
        # Fetch all airports in the specified continent for the game
        airports_query = f"""
            SELECT airport_id 
            FROM airport_info 
            LEFT JOIN airport ON airport.ident = airport_info.airport_id 
            WHERE airport.continent = '{continent}' 
            AND airport_info.game_id = {game_id};
        """
        airports = run(airports_query)

        if not airports:
            return jsonify(
                {"success": False, "message": f"No airports found in continent {continent} for game {game_id}."}), 404

        # Calculate the number of airports to close
        open_airports_query = f"""
            SELECT COUNT(*) 
            FROM airport_info 
            LEFT JOIN airport ON airport.ident = airport_info.airport_id 
            WHERE airport.continent = '{continent}' 
            AND airport_info.infected = 0 
            AND airport_info.closed = 0 
            AND airport_info.game_id = {game_id};
        """
        count = run(open_airports_query)[0][0]

        if count == 0:
            return jsonify({"success": False,
                            "message": f"No open airports found in continent {continent} for game {game_id}."}), 404

        # Calculate public dissatisfaction increase
        dissatisfaction_increase = int(6.5 * (count ** (1 / 1.65)))

        # Close all open airports in the continent
        close_airports_query = f"""
            UPDATE airport_info 
            SET closed = 1 
            WHERE airport_id IN (
                SELECT airport_id 
                FROM airport_info 
                LEFT JOIN airport ON airport.ident = airport_info.airport_id 
                WHERE airport.continent = '{continent}' 
                AND airport_info.infected = 0 
                AND airport_info.closed = 0 
                AND airport_info.game_id = {game_id}
            ) 
            AND game_id = {game_id};
        """
        run(close_airports_query)

        # Update game state
        game_update_query = f"""
            UPDATE saved_games 
            SET public_dissatisfaction = LEAST(100, public_dissatisfaction + {dissatisfaction_increase}) 
            WHERE id = {game_id};
        """
        run(game_update_query)

        return jsonify({
            "success": True,
            "message": f"Closed {count} airports in continent {continent}.",
            "dissatisfaction_increase": dissatisfaction_increase,
            "closed_airports": count
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.route('/api/games/<int:game_id>/new_turn', methods=['POST'])
def new_game_turn(game_id):
    """
    Advances the game to a new turn, updates game variables, and saves them to the database.
    """
    try:
        # Fetch current game state
        game_query = f"""
            SELECT money, infected_population, public_dissatisfaction, research_progress, 
                   game_turn, infection_rate, max_distance
            FROM saved_games 
            WHERE id = {game_id};
        """
        game_state = run(game_query)
        if not game_state:
            return jsonify({"success": False, "message": "Game not found."}), 404

        # Unpack game state
        money, infected_population, public_dissatisfaction, research_progress, \
        game_turn, infection_rate, max_distance = game_state[0]

        # Fetch infected airports count
        infected_airports_query = f"""
            SELECT COUNT(*) FROM airport_info 
            WHERE infected = 1 AND game_id = {game_id};
        """
        infected_airports = run(infected_airports_query)[0][0]

        # Apply formulas to update game variables
        max_distance += random.randint(-10, 100)  # Adjust max distance randomly
        constant_growth = 10
        infected_population = infected_population + int(infected_airports / 30 * constant_growth)
        infected_population = min(infected_population, infected_airports * 10 / 3)  # Cap infected population
        coeff = 3 * random.random()
        public_dissatisfaction = int(
            public_dissatisfaction + (coeff ** ((public_dissatisfaction + infected_population) / 20))
        )
        public_dissatisfaction = min(public_dissatisfaction, 100)  # Cap dissatisfaction at 100
        money = money + int(
            random.randint(0, 1000) + (2 * (100 - public_dissatisfaction) / 100) * (100 - infected_population) * 100
        )

        # Increment game turn
        game_turn += 1

        # Update game state in the database
        update_query = f"""
            UPDATE saved_games 
            SET money = {money}, 
                infected_population = {infected_population}, 
                public_dissatisfaction = {public_dissatisfaction}, 
                max_distance = {max_distance}, 
                game_turn = {game_turn}
            WHERE id = {game_id};
        """
        run(update_query)

        # Return updated game state
        return jsonify({
            "success": True,
            "message": f"Advanced to turn {game_turn}.",
            "updated_game_state": {
                "game_turn": game_turn,
                "money": money,
                "infected_population": infected_population,
                "public_dissatisfaction": public_dissatisfaction,
                "max_distance": max_distance
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/games/<int:game_id>/infection_spread', methods=['POST'])
def api_infection_spread(game_id):
    """
    Spreads infection from infected airports to nearby airports for the specified game.
    """
    try:
        # Fetch the infection rate for the specified game from the database
        infection_rate_query = f"""
            SELECT infection_rate 
            FROM saved_games 
            WHERE id = {game_id};
        """
        infection_rate_result = run(infection_rate_query)

        if not infection_rate_result:
            return jsonify({"success": False, "message": f"Game ID {game_id} not found."}), 404

        infection_rate = infection_rate_result[0][0]

        # Call the infection spread function
        result = infection_spread(game_id, infection_rate)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/games/<int:game_id>/random_event', methods=['POST'])
def random_event(game_id):
    """
    Handles a random event in the game.
    """
    try:
        # 60% probability of no event
        if random.random() < 0.6:
            return jsonify({
                "success": True,
                "event": "Nothing special happened this time."
            }), 200

        # Load Gemini model
        gemini_model = GeminiModel()

        # Load the random event prompt from a YAML or hardcoded string
        random_event_prompt = (
            "Generate details for a single random event in a strategy game where the player manages global variables "
            "like money, infected population, and public dissatisfaction. The event should include a title, a short "
            "description, and changes to the variables (Money: ±X, Infected: ±X, Dissatisfaction: ±X). Provide only one "
            "event per request. DO NOT provide any other information.\n\n"
            "Your answer MUST have this structure:\n\n"
            "Title: {title}\n\n"
            "Description: {description}\n\n"
            "Money: {money}\n\n"
            "Infected: {infected}\n\n"
            "Dissatisfaction: {dissatisfaction}"
        )

        # Call Gemini to generate the random event
        gemini_response = gemini_model.call_model(user_prompt=random_event_prompt)

        # Parse Gemini response
        lines = gemini_response.splitlines()
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

        # Fetch current game state
        game_query = f"SELECT money, infected_population, public_dissatisfaction FROM saved_games WHERE id = {game_id};"
        game_state = run(game_query)
        if not game_state:
            return jsonify({"success": False, "message": "Game not found."}), 404

        # Update game state based on the event
        money, infected_population, public_dissatisfaction = game_state[0]
        updated_money = max(0, money + parsed_event["money"])
        updated_infected_population = max(0, infected_population + parsed_event["infected"])
        updated_public_dissatisfaction = max(0, min(100, public_dissatisfaction + parsed_event["dissatisfaction"]))

        # Save updated game state to DB
        update_query = f"""
            UPDATE saved_games
            SET money = {updated_money}, 
                infected_population = {updated_infected_population}, 
                public_dissatisfaction = {updated_public_dissatisfaction}
            WHERE id = {game_id};
        """
        run(update_query)

        # Respond with the event details and updated variables
        return jsonify({
            "success": True,
            "event": parsed_event,
            "updated_game_state": {
                "money": updated_money,
                "infected_population": updated_infected_population,
                "public_dissatisfaction": updated_public_dissatisfaction
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Run the Flask development server; line below needed in order not to run app.py when imporing to other scripts
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Specify the host and port