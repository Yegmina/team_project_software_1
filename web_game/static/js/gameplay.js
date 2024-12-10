'use strict';
// Map initializing
let options = {
    inertia: true,
    inertiaMaxSpeed: 1000,
    keyboard: true,
    zoomControl: false,
    // center: L.latLng(50, 100),
}
const map = L.map('map', options).setView([45, 10], 2.5);
let corner1 = L.LatLng(-180, -90)
let corner2 = L.LatLng(180, 90)
let bounds = L.LatLngBounds(corner2, corner1);
map.setMaxBounds(bounds);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    minZoom: 2.0,
    maxZoom: 2.0,
}).addTo(map);

// Game Variable

let body = document.querySelector("body");
let game_data_holder = document.querySelector("#sneaky-data");
let game_data = JSON.parse(game_data_holder.innerText);
const game_id = game_data[0].id;
let all_airports
console.log(game_id);

body.removeChild(game_data_holder);
//

// Utilities
const timer = ms => new Promise(res => setTimeout(res, ms));
//

async function gameInitialize() {
    console.log(`Game Initalize`)
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            update_new_game_stats(game_data[0]);
            update_progress_bars(game_data[0]);
            console.log(game_data[0]);
            const other_choices = document.querySelector("#other-choices");
            const skip_turn = document.createElement('button');

            // Skip turn button
            skip_turn.id = "skip-turn";

            skip_turn.innerText = 'Skip this turn (Do nothing)';
            other_choices.appendChild(skip_turn);

            skip_turn.addEventListener("mouseover", () => {
                skip_turn.style.borderColor = `red`;
            })
            skip_turn.addEventListener("mouseout", () => {
                skip_turn.style.borderColor = `black`;
            })
            skip_turn.addEventListener("mousedown", () => {
                skip_turn.style.backgroundColor = `gray`;
            })
            skip_turn.addEventListener("mouseup", () => {
                skip_turn.style.backgroundColor = `white`;
            })
            // End skip turn button

            //Start Static Airport data
            let retries = 5, seconds = 500;
            let success = false;
            while (!success && retries--) {
                try {
                    all_airports = await fetch(`/api/airports/${game_id}`)
                    all_airports = await all_airports.json()
                    success = all_airports.success;
                } catch (err) {
                    console.log(`Fetching airports info from game ${game_id} failed: ${err}.`)
                } finally {
                    if (!success) {
                        seconds *= 2;
                        console.log(`Trying to fetch from /api/airports/${game_id} again in ${seconds / 1000}`);
                        await timer(seconds);
                    }
                }
            }
            console.log(`Fetched airports ${all_airports.success ? 'successfully' : 'failed'}`)
            console.log(all_airports)

            //End Static Airport data

            // Minimize button
            const panel_minimize = document.querySelector("#panel-minimize");
            const minimize_btn = document.createElement("button");

            panel_minimize.appendChild(minimize_btn);

            minimize_btn.innerText = `--`
            minimize_btn.addEventListener('click', async () => {
                document.querySelector('#panel').style.display = 'none';
            })
            // End minimize button

            // Panel reopen button
            const open_choice_panel = document.querySelector("#open-choice-panel");
            const reopen_btn = document.createElement("button");

            open_choice_panel.appendChild(reopen_btn);
            open_choice_panel.style = `
                display: flex;
                align-content: center;
                justify-content: center;
            `

            reopen_btn.innerText = `Available options`;
            reopen_btn.style = `
                height: 100px;
                align-self: center;
            `
            reopen_btn.addEventListener('click', async () => {
                document.querySelector("#panel").style.display = 'flex';
            })

            resolve();
        })
    })

}

function story() {
    return;
}

async function fetchChoice() {
    /* 
    This function will get all available choices from a game
    that the player haven't made. (Dunno why should this be but
    it's a feature nonetheless) ;)
     */
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            let success = false;
            let retries = 5, wait_length = 500;
            while (!success && retries--) {
                try {
                    var all_available_choices = await fetch(`/api/games/${game_id}/make_choice`);
                    all_available_choices = await all_available_choices.json()
                    success = all_available_choices.success;
                    if (success) {
                        console.log("Successfully executed make_choice api");
                        break;
                    }
                } catch (error) {
                    console.error(`Error fetching game with /api/games/game_id/make_choice: ${error}`);
                } finally {
                    if (!success) {
                        wait_length *= 2;
                        console.log(`Trying fetching from /api/games/${game_id}/make_choice again in ${wait_length / 1000} seconds.`)
                        await timer(wait_length);
                    }
                }
            }
            resolve(all_available_choices.choices);
        })
    })
}

function filterChoice(all_choices) {
    const filtered_choices = [];
    let check_array = new Array(all_choices.length + 1).fill(false);
    let possible_choices = Math.min(3, all_choices.length);
    for (let i = 0; i < possible_choices; i++) {
        while (true) {
            let random_number = Math.round(Math.random() * (all_choices.length))
            if (random_number === all_choices.length) random_number -= 1;
            if (check_array[random_number] === false) {
                check_array[random_number] = true;
                filtered_choices.push(all_choices[random_number]);
                break;
            }
        }
    }
    return filtered_choices;
}

async function renderChoice() {
    /* 
    In order for the player to make choice, we need:
    1. Load all existing choices that the player haven't made
    2. Choose 3/5 from the list
    3. Show them on the screen (preferably a Panel, or something that 
    pop ups and let the player choose)
    4. Return the formatted data of the choice as the return value
    */
    // Step 1
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            console.log("RENDER CHOICE FUNCTION INITIATED");
            let retries = 3, seconds = 1;
            while (retries--) {
                try {
                    var all_choices = await fetchChoice();
                } catch (err) {
                    console.log(`fetchChoice() failed to fetch data: ${err}.`)
                    console.log(`Retrying after ${seconds} seconds.`)
                }
            }
            // Step 2
            const filtered_choices = filterChoice(all_choices);
            for (let item of filtered_choices) {
                console.log(item);
            }

            // Step 3
            // document.querySelector(`
            //     .leaflet-tile-pane
            // `).style.opacity = 0.5

            const panel = document.querySelector('#panel');
            panel.style.display = 'flex';
            let itemList = document.querySelector(".item-list")
            itemList.innerHTML = '';
            let warning = document.querySelector("#possible-warning");
            warning.innerText = '';
            for (let choice of filtered_choices) {
                let article = document.createElement('article');
                let h2 = document.createElement('h2');
                let p = document.createElement('p');

                article.choice_id = choice.id;

                h2.innerText = choice.name;
                p.innerText = `Cost: ${choice.cost} moni`;

                article.style = `
                    width: ${(90 - filtered_choices.length * 2) / filtered_choices.length}%;
                    margin : 1%;
                    height : 16rem;
                    border-radius : 8px;
                    border: solid green;
                `;
                article.appendChild(h2);
                article.appendChild(p);

                itemList.appendChild(article);
            }

            resolve(filtered_choices);
            // dev note: ADD CHOICE OF DOING NOTHING AS A SMALL BUTTON
        })
    })
}
async function getUserChoice() {
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            console.log("GET USER CHOICE FUNCTION INITIATED");
            const all_choices_on_panel = document.querySelectorAll('article');
            for (let choice of all_choices_on_panel) {
                // Choice :: Article 
                choice.addEventListener('mouseover', () => {
                    choice.style.border = `solid red`;
                })
                choice.addEventListener('mouseout', () => {
                    choice.style.border = 'solid green';
                })
                choice.addEventListener('mousedown', () => {
                    choice.style.backgroundColor = 'gray';
                })
                choice.addEventListener('mouseup', () => {
                    choice.style.backgroundColor = 'white';
                })
                choice.addEventListener('click', async () => {
                    let choice_id = choice.choice_id;
                    let success = false;
                    let retries = 5, wait_length = 500;
                    while (!success && retries--) {
                        try {
                            var response = await fetch(`/api/games/${game_id}/process_choice`, {
                                method: 'POST',
                                body: JSON.stringify({
                                    "choice_id": choice_id,
                                }),
                                headers: {
                                    "Content-Type": "application/json",
                                }
                            })
                            response = await response.json();
                            success = response.success;
                            if (success) {
                                document.querySelector('#panel').style.display = 'none';
                                console.log(response.message);
                                console.log(`User chose: ${choice_id}.`);
                                resolve(`{"status": "User chose ${choice_id}", "value": 100}`)
                            }
                            else if (!success) {
                                document.querySelector('#possible-warning').innerText = response.message;
                            }
                        } catch (err) {
                            document.querySelector('#possible-warning').innerText = err;
                        } finally {
                            if (!success && !(response.err == 400)) {
                                wait_length *= 2;
                                console.log(`Trying /api/games/${game_id}/process_choice again in ${wait_length / 1000} seconds.`)
                                await timer(wait_length);
                            }
                        }
                    }
                })
            }
            let skip_turn = document.querySelector("#skip-turn")
            skip_turn.addEventListener("click", () => {
                let panel = document.querySelector('#panel');
                panel.style.display = 'none';
                resolve(`{"status": "Turn skipped", "value": 101}`)
            })
        })
    })
}

async function game_execute(choice) {
    console.log("This indicates that the function is being called: ", choice);
    console.log(choice);
    let success = false;
    let retries = 5;
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            while (!success && retries--) {
                try {
                    // HERE IS THE BEAST THAT'S BEEN BUGGING ME I DON'T KNOW WHY
                    // THIS LINK DOESN'T WORK BUT AHDHWAWDHAHWDHAWDHAWHDHH IT JUST DOESN'T
                    // WANT TO WORK
                    console.log(choice.id);
                    var response = await fetch(`/api/games/${game_id}/process_choice`, {
                        method: 'POST',
                        body: JSON.stringify({
                            "choice_id": choice.id,
                        }),
                        headers: {
                            "Content-Type": 'application/json',
                        }
                    });
                    response = await response.json();
                    console.log(response.message);
                    success = response.success;
                } catch (err) {
                    console.log(`Error while process choice of game from /api/games/${game_id}/process_choice`, err);
                }
            }
            resolve(response);
        })
    })
}



async function next_turn() {
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            let success = false;
            let retries = 5, wait_length = 500;
            while (!success && retries--) {
                try {
                    var response = await fetch(`/api/games/${game_id}/new_turn`, {
                        method: 'POST',
                    })
                    response = await response.json()
                    console.log(response);
                    success = response.success;

                    const current_game_stats = await response.updated_game_state;
                    await update_new_game_stats(current_game_stats);
                    update_progress_bars(current_game_stats);

                    resolve(`{"status": "Turn advanced successfully", "value": 100}`)
                } catch (err) {
                    console.log("Error while computing next game turn's variables:", err);
                } finally {
                    if (!success) {
                        wait_length *= 2;
                        console.log(`Trying fetching from /api/games/${game_id}/new_turn in ${wait_length / 1000} seconds.`)
                        await timer(wait_length);
                    }
                }
            }
            resolve();
        })
    })
}

async function update_new_game_stats(stats) {
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            let game_turn = document.querySelector("#game-turn")
            let game_money = document.querySelector("#game-money")
            let game_inf_airports = document.querySelector("#game-inf-airports");



            game_turn.innerText = stats.game_turn;
            game_money.innerText = stats.money;


            let retries = 3, success = false, wait_length = 500;

            let game_inf_airports_num = 0;


            while (!success && retries--) {
                try {
                    let game_airports_info = await fetch(`/api/airports/${game_id}`);
                    game_airports_info = await game_airports_info.json();
                    success = game_airports_info.success;
                    if (success) {
                        game_inf_airports = game_airports_info.airports;
                        for (let airport of game_inf_airports) {
                            if (airport.infected) {
                                game_inf_airports_num++;
                            }
                        }
                    }
                } catch (err) {
                    console.log(`ERROR while fetching from /api/airports/${game_id}: ${err}`);

                } finally {
                    if (!success) {
                        wait_length *= 2;
                        console.log(`Trying fetching from /api/airports/${game_id} again in ${wait_length / 1000} seconds.`);
                        await timer(wait_length);
                    }
                }
            }

            game_inf_airports.innerText = game_inf_airports_num;

            resolve();
        })
    })
}

async function update_progress_bars(stats) {
    const dis_progress = document.querySelector("#dis-progress");
    dis_progress.style.width = stats.public_dissatisfaction + '%';

    const cure_progress = document.querySelector("#cure-progress");
    cure_progress.style.width = stats.research_progress + '%';

    const inf_progress = document.querySelector("#inf-progress");
    inf_progress.style.width = stats.infected_population + '%';
}
// start_game();

async function place_markers() {
    console.log(`Place_markers`);
    return new Promise(async function (resolve) {
        setTimeout(async function () {
            const markers = L.featureGroup().addTo(map)
            for (let i = 0; i < all_airports.airports.length; i++) {
                let icao = all_airports.airports[i].airport_id

                let retries = 3, seconds = 1, success = false;
                while (!success && retries--) {
                    try {
                        var airport_info = await fetch(`/api/airports/info/${icao}`)
                        airport_info = await airport_info.json()
                        success = airport_info.success;
                        console.log(success)
                    } catch (err) {
                        console.log(`Fetch airport ${icao} data failed: ${err}`);
                        console.log(`Trying again after ${seconds}.`)
                    } finally {
                        if (!success) {
                            console.log(`Trying to fetch from /api/airports/info/${icao} again in ${seconds} seconds.`);
                            await timer(seconds);
                            seconds *= 2;
                        }
                    }
                }
                let log = airport_info.airport.longitude_deg
                let lat = airport_info.airport.latitude_deg
                const marker = L.marker([lat, log]).addTo(map)
                marker._icon.classList.add("huechange" + `${i}`);
                markers.addLayer(marker)
                map.setView([lat, log])

                //const placeName=document.createElement("h3")
                //placeName.innerText = airport_info.airports[i]
            }
            resolve();
        })
    })
}

function recolor_map_pins(isInfected) {
  // Get all elements with the class 'huechange'
  let pins = document.getElementsByClassName('huechange');

  // Check if there are any elements
  if (pins.length === 0) {
    console.warn("No pins found with the class 'huechange'.");
    return;
  }

  // Apply the appropriate filter based on infection status
  for (let pin of pins) {
    pin.style.filter = isInfected ? 'hue-rotate(210deg)' : 'hue-rotate(60deg)';
  }
}

async function gameLoop() {
    /* 
    Holds all of the real-time game functionality 
    Each turn consists of 3 basic phase : 
    - Choices phase : Player makes choice 
    - Active phase : The game process said choice and change the game's statistics
    accordingly
    - Passive phase : The GeminiAI will decide if this round will occur a
    random events or not and said event will be generated by the AI.
    */
    console.log("Now inside GameLoop");
    await gameInitialize();
    await timer(1000);
    await place_markers();
    recolor_map_pins(true)

    while (true) {

        await renderChoice()
            .then(getUserChoice)
            // .then(random_event)
            .then(next_turn);
    }


    // let all_choices = await renderChoice(); // Choices phase
    // let user_choice = await getUserChoice()

}


gameLoop()



/* 
story / dev commentary or something (just a feature)
story()
while(1 === 1) {
    gameLoop();
}
*/