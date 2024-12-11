# Apocalypse Strategy Game

## Table of Contents
- [Overview](#overview)
- [Gameplay](#gameplay)
- [Features](#features)
- [Project Structure](#project-structure)
- [How to Run the Game](#how-to-run-the-game)
- [API Documentation](#api-documentation)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)
- [Links](#links)

---

## Overview

**Apocalypse Strategy Game** is an interactive web-based strategy game where players manage a world on the brink of disaster. Players must make critical decisions to balance economic resources, research a cure for a spreading infection, and manage public dissatisfaction, all while combating the rapidly growing pandemic.

### Objective:
- Prevent the infection from spreading worldwide.
- Develop a cure while maintaining global stability.
- Keep public dissatisfaction from spiraling into chaos.

---

## Gameplay

The game provides an immersive decision-making experience:

1. **Turn-Based System**: Each turn, players choose from several actions, such as investing in research, closing airports, or handling public dissatisfaction.
2. **Variables**:
   - **Money**: Resource management for funding operations.
   - **Infected Population**: Tracks the global infection level.
   - **Public Dissatisfaction**: Reflects societal unrest.
   - **Cure Progress**: Indicates progress toward curing the infection.
3. **Random Events**: Dynamic in-game events randomly impact variables, forcing players to adapt strategies.
4. **Map Interface**: Visualize the spread of infection on a world map with airports as key points.

---

## Features

- **Interactive World Map**: Built using the Leaflet.js library for real-time tracking of infection spread.
- **Dynamic Decision Making**: Players select from randomly generated actions each turn.
- **Random Events**: Randomized global events (e.g., disasters, breakthroughs) impact variables.
- **Data Persistence**: Game states are saved to a MySQL database, enabling users to resume saved games.
- **AI Integration**: The Gemini AI generates random events to enhance replayability.

---

## Project Structure

```
web_game/
│
├── archive/                  # Deprecated or archived content
├── .cph/                     # IDE configuration files
├── random_events/            # Random events definition
│   ├── examples.txt          # Example random events for testing
│
├── static/                   # Static files
│   ├── css/                  # Stylesheets
│   ├── img/                  # Images
│   ├── js/                   # JavaScript files
│
├── templates/                # HTML templates
│   ├── index.html            # Home page template
│   ├── gameplay.html         # Gameplay interface
│   ├── game_details.html     # Game details page
│   ├── new_game.html         # New game creation page
│
├── utils/                    # Utility scripts
│   ├── ai/                   # AI integration
│   │   ├── gemini.py         # Random event generation logic
│   ├── functions.py          # Core game logic and database interactions
│
├── app.py                    # Main Flask application entry point
├── README.md                 # Project documentation (this file)
└── requirements.txt          # Python dependencies
```

---

## How to Run the Game

### Prerequisites:
1. Python 3.8 or higher installed on your system.
2. MySQL server for the database.
3. Install dependencies using `pip`.

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Yegmina/team_project_software1-2.git
   cd team_project_software1-2
   ```

2. **Install Dependencies**:
Right now we don't have requirements.txt, but we are going to add it (or you can help us by generating it).
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**:
   - Update database credentials in `utils/functions.py` with your database.
   - Run the `all sql from sql_initial folder` queries to initialize tables.
   - Change gemini api key in gemini.py (you can implement .env var. but now it is hardcoded).

4. **Start the Server**:
   ```bash
   python app.py
   ```

5. **Access the Game**:
   Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## API Documentation

### Core Endpoints:

#### Game Management

1. **Home Page**  
   - **GET `/`**  
     **Description**: Displays the homepage with a list of all saved games and options to create a new game.  
     **Response**:  
     - **Success**: Render `index.html` with games list.  
     - **Error**: JSON error message.  

---

2. **Create New Game**  
   - **POST `/new_game`**  
     **Description**: Creates a new game profile with a given name.  
     **Request Body**:  
     ```json
     { "name": "Game Name" }
     ```
     **Response**:  
     - **Success**: Redirects to `/play/<game_id>`.  
     - **Error**: Displays the `new_game.html` template with an error message.  

---

3. **Resume Game**  
   - **GET `/resume_game`**  
     **Description**: Displays a list of saved games for resumption.  
     **Response**:  
     - **Success**: Render `resume_game.html`.  
     - **Error**: JSON error message.  

---

4. **Fetch Game Details**  
   - **GET `/fetch_game/<int:game_id>`**  
     **Description**: Fetches details of a specific game by ID.  
     **Response**:  
     - **Success**: Renders `game_details.html` with the game data.  
     - **Error**: JSON error message.  

---

#### Development APIs

1. **Fetch Game Details (Dev)**  
   - **GET `/dev/fetch_games/<int:id>`**  
     **Description**: Returns game details for the given ID in raw JSON format.  
     **Response**:  
     - **Success**: JSON with game data.  
     - **Error**: JSON error message.  

---

2. **Check Game Existence**  
   - **GET `/dev/game_exists/<game_name>`**  
     **Description**: Checks if a game with the specified name exists.  
     **Response**:  
     - **Success**: JSON with game existence status.  
     - **Error**: JSON error message.  

---

#### Gameplay APIs

1. **Play Game**  
   - **GET `/play/<game_id>`**  
     **Description**: Loads the gameplay interface for a specific game ID.  
     **Response**:  
     - **Success**: Render `gameplay.html` with game data.  
     - **Error**: JSON error message.  

---

2. **Search Game by Name**  
   - **GET `/api/games/search`**  
     **Description**: Searches for games by name.  
     **Query Parameter**: `name=Game Name`  
     **Response**:  
     - **Success**: JSON with matching games.  
     - **Error**: JSON error message.  

---

3. **Check Game Status**  
   - **GET `/api/games/<int:game_id>/check_status`**  
     **Description**: Checks the current game status and updates the `game_over` flag if applicable.  
     **Response**:  
     - **Success**: JSON with status and message.  
     - **Error**: JSON error message.  

---

4. **Fetch Available Choices**  
   - **GET `/api/games/<int:game_id>/make_choice`**  
     **Description**: Returns all available choices for the current turn in the game.  
     **Response**:  
     - **Success**: JSON with available choices.  
     - **Error**: JSON error message.  

---

5. **Process Player's Choice**  
   - **POST `/api/games/<game_id>/process_choice`**  
     **Description**: Processes the player's choice and updates the game state.  
     **Request Body**:  
     ```json
     { "choice_id": 1 }
     ```  
     **Response**:  
     - **Success**: JSON with updated game state.  
     - **Error**: JSON error message.  

---

6. **Close Specific Airport**  
   - **POST `/api/airports/close`**  
     **Description**: Closes a specified airport and updates the game's money and public dissatisfaction levels.  
     **Request Body**:  
     ```json
     { "game_id": 1, "airport_id": "JFK" }
     ```  
     **Response**:  
     - **Success**: JSON with updated airport and game states.  
     - **Error**: JSON error message.  

---

7. **Fetch All Airports**  
   - **GET `/api/airports/<int:game_id>`**  
     **Description**: Returns all airports in the game with their statuses.  
     **Response**:  
     - **Success**: JSON with airport and global game data.  
     - **Error**: JSON error message.  

---

8. **Fetch Airport Details**  
   - **GET `/api/airports/info/<string:airport_id>`**  
     **Description**: Fetches detailed information for a specific airport.  
     **Response**:  
     - **Success**: JSON with airport and game-related data.  
     - **Error**: JSON error message.  

---

9. **Close Airports by Continent**  
   - **POST `/api/airports/close_continent`**  
     **Description**: Closes all airports in a specific continent for a game.  
     **Request Body**:  
     ```json
     { "game_id": 1, "continent": "EU" }
     ```  
     **Response**:  
     - **Success**: JSON with updated game data.  
     - **Error**: JSON error message.  

---

10. **Advance to New Turn**  
    - **POST `/api/games/<int:game_id>/new_turn`**  
      **Description**: Advances the game to the next turn and updates all variables.  
      **Response**:  
      - **Success**: JSON with updated game state.  
      - **Error**: JSON error message.  

---

11. **Spread Infection**  
    - **POST `/api/games/<int:game_id>/infection_spread`**  
      **Description**: Handles the spread of infection from infected airports.  
      **Response**:  
      - **Success**: JSON with infection spread details.  
      - **Error**: JSON error message.  

---

12. **Trigger Random Event**  
    - **POST `/api/games/<int:game_id>/random_event`**  
      **Description**: Triggers a random event in the game with a 40% chance of occurrence.  
      **Response**:  
      - **Success**: JSON with event details.  
      - **Error**: JSON error message.  
---

## Technology Stack

### Backend:
- **Flask**: Python micro-framework for routing and backend logic.
- **MySQL**: Relational database for storing game data.
- **Gemini**: Using Gemini AI APIs to generate random events. 
Using AI to improve in-game experience and making game more unpredictable and fun.

### Frontend:
- **HTML/CSS**: Responsive user interfaces.
- **JavaScript (Vanilla)**: Game logic and interaction.
- **Leaflet.js**: World map visualization.

---

## Contributing

We welcome contributions to enhance the game! Follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature description"`.
4. Push to your branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Links

- **GitHub Repository**: [Apocalypse Strategy Game](https://github.com/Yegmina/team_project_software1-2)

Enjoy saving the world!
Having fun while coding!