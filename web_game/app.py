
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from utils.functions import *  # Import all functions from functions.py
import json

app = Flask(__name__)

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
        name = request.form.get('name')
        response, status = new_game(name)
        if status == 201:
            return redirect(url_for('index'))
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


# Run the Flask development server; line below needed in order not to run app.py when imporing to other scripts
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Specify the host and port
