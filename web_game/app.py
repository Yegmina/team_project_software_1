import random

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from flask_cors import CORS

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






# Run the Flask development server; line below needed in order not to run app.py when imporing to other scripts
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Specify the host and port
