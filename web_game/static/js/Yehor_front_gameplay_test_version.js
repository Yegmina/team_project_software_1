// .then will be switched to async, onclinc to event

//CHOICE MAKING
function fetchChoices(gameId) {
    fetch(`/api/games/${gameId}/make_choice`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderChoices(data.choices);
            } else {
                console.error("Failed to fetch choices:", data.error);
            }
        })
        .catch(err => console.error("Error fetching choices:", err));
}

function renderChoices(choices) {
    const targetOutput = document.getElementById("target-output");
    targetOutput.innerHTML = ""; // Clear previous choices
    choices.forEach(choice => {
        const choiceButton = document.createElement("button");
        choiceButton.innerText = `${choice.name} (Cost: ${choice.cost})`;
        choiceButton.onclick = () => processChoice(choice.id);
        targetOutput.appendChild(choiceButton);
    });
}

function processChoice(choiceId) {
    const gameId = getCurrentGameId(); // Retrieve the current game ID
    fetch(`/api/games/${gameId}/process_choice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ choice_id: choiceId }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                updateGameState(data.updated_game_state); // Update the UI
                triggerRandomEvent(gameId); // Trigger random events
            } else {
                alert(`Choice failed: ${data.message}`);
            }
        })
        .catch(err => console.error("Error processing choice:", err));
}



// NEW TURN
function advanceTurn(gameId) {
    fetch(`/api/games/${gameId}/new_turn`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateGameState(data.updated_game_state); // Update the UI
                triggerRandomEvent(gameId); // Trigger random events
            } else {
                alert("Failed to advance turn: " + data.message);
            }
        })
        .catch(err => console.error("Error advancing turn:", err));
}


//INFECTION SPREADING
function spreadInfection(gameId) {
    fetch(`/api/games/${gameId}/infection_spread`, {
        method: "POST",
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Infection spread completed.");
                updateAirports(data.all_airports);
            } else {
                alert("Infection spread failed: " + data.message);
            }
        })
        .catch(err => console.error("Error spreading infection:", err));
}

function updateAirports(airports) {
    airports.forEach(airport => {
        const marker = getAirportMarker(airport.airport_id); // Implement this to retrieve map markers
        if (airport.infected) {
            marker.setIcon(infectedIcon); // Assume infectedIcon is defined
        }
        if (airport.closed) {
            marker.setIcon(closedIcon); // Assume closedIcon is defined
        }
    });
}

//RANDOM EVENTS
function triggerRandomEvent(gameId) {
    fetch(`/api/games/${gameId}/random_event`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.event && data.event.title) {
                    // Display the random event
                    const event = data.event;
                    alert(`Event: ${event.title}\n${event.description}`);

                    // Directly update the game state from the response
                    updateGameState(data.updated_game_state);
                } else {
                    // If no random event occurs, log or skip
                    console.log("No random event occurred this turn.");
                }
            } else {
                console.error("Random event error:", data.message);
            }
        })
        .catch(err => console.error("Error triggering random event:", err));
}



function refetchGameState(gameId) {
    fetch(`/api/games/${gameId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateGameState(data.game); // Update UI with the new game state
            } else {
                console.error("Failed to fetch game state:", data.message);
            }
        })
        .catch(err => console.error("Error fetching game state:", err));
}

//GAME STATISTIC UUPDATE
function updateGameState(state) {
    const defaultState = {
        game_turn: 0,
        money: 0,
        public_dissatisfaction: 0,
        infected_population: 0,
        research_progress: 0,
    };

    const {
        game_turn = 0,
        money = 0,
        public_dissatisfaction = 0,
        infected_population = 0,
        research_progress = 0,
    } = { ...defaultState, ...state };

    document.querySelector("#game-info").innerHTML = `
        <p>
            Money: ${money}<br>
            Public dissatisfaction: ${public_dissatisfaction}<br>
            Infected population: ${infected_population}
        </p>
    `;

    document.getElementById("dis-progress").style.width = `${public_dissatisfaction}%`;
    document.getElementById("cure-progress").style.width = `${research_progress}%`;
    document.getElementById("inf-progress").style.width = `${infected_population}%`;
}


//EVENTS HOOKS
document.addEventListener("DOMContentLoaded", () => {
    const gameId = getCurrentGameId(); // Implement to get game ID
    fetchChoices(gameId);
    document.getElementById("new-turn-btn").onclick = () => advanceTurn(gameId);
    document.getElementById("spread-infection-btn").onclick = () => spreadInfection(gameId);
    document.getElementById("random-event-btn").onclick = () => triggerRandomEvent(gameId);
});


function getCurrentGameId(){
  return 149
}