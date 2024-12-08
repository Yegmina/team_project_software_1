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

// Something else

let body = document.querySelector("body");
let game_data_holder = document.querySelector("#sneaky-data");
let game_data = JSON.parse(game_data_holder.innerText);
const game_id = game_data[0].id;
console.log(game_id);

body.removeChild(game_data_holder);

function story() {
    return;
}

async function fetchChoice() {
    /* 
    This function will get all available choices from a game
    that the player haven't made. (Dunno why should this be but
    it's a feature nonetheless) ;)
     */

    let success = false;
    let retries = 5;
    while (!success && retries--) {
        try {
            var all_available_choices = await fetch(`/api/games/${game_id}/make_choice`);
            all_available_choices = await all_available_choices.json()
            success = all_available_choices.success;
        } catch (error) {
            console.error(`Error fetching game with /api/games/game_id/make_choice: ${error}`);
        }
    }
    return all_available_choices.choices;
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

async function makeChoice() {
    /* 
    In order for the player to make choice, we need:
    1. Load all existing choices that the player haven't made
    2. Choose 3/5 from the list
    3. Show them on the screen (preferably a Panel, or something that 
    pop ups and let the player choose)
    4. Return the formatted data of the choice as the return value
    */

    // Step 1
    const all_choices = await fetchChoice();

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
    for (let choice of filtered_choices) {
        let article = document.createElement('article');
        let h2 = document.createElement('h2');
        let p = document.createElement('p');

        h2.innerText = choice.name;
        p.innerText = choice.cost;

        article.style = `
            width: ${(100 - filtered_choices.length * 2) / filtered_choices.length}%;
            margin : 1%;
            height : 16rem;
            border-radius : 8px;
            border: gray;
        `;
        article.appendChild(h2);
        article.appendChild(p);
        article.addEventListener('click', () => {

            // dev note : process_choice : `/api/games/game_id/process_choice`, method POST
            if (choice.cost <= game_data[0].money) {
                console.log(`You chose the choice of id: ${choice.id}: ${choice.name} || Costed : ${choice.cost}`)
                panel.style.display = 'none';
                document.querySelector(`
                    .leaflet-tile-pane
                `).style.opacity = 1;

                game_execute(choice); // Execute Choice
            }
            else {
                console.log("haha loser");
            }
            /* Player chose the choice --> Action phase  */
        })
        itemList.appendChild(article);
    }

    // dev note: ADD CHOICE OF DOING NOTHING AS A SMALL BUTTON
}

async function game_execute(choice) {
    console.log("This indicates that the function is being called: ", choice);
    console.log(choice);
    let success = false;
    let retries = 5;
    while (!success && retries--) {
        try {
            // HERE IS THE BEAST THAT'S BEEN BUGGING ME I DON'T KNOW WHY
            // THIS LINK DOESN'T WORK BUT AHDHWAWDHAHWDHAWDHAWHDHH IT JUST DOESN'T
            // WANT TO WORK
            console.log(choice.id);
            let response = await fetch(`/api/games/${game_id}/process_choice`, {
                method: 'POST',
                body: JSON.stringify({
                    'choice_id': choice.id,
                }),
                headers: {
                    "Content-Type": 'application/json',
                }
            })
            console.log(response.message);
            success = response.success;
        } catch (err) {
            console.log("Error while process choice of game:", err);
        }
    }
}

async function next_turn() {
    let success = false;
    let retries = 5;
    while (!success && retries--) {
        try {
            let response = await fetch(`/api/games/${game_id}/new_turn`, {
                method: 'POST',
            })
            response = await response.json()
            console.log(response);
            success = response.success;

            const current_game_stats = response.updated_game_state;
            update_new_game_stats(current_game_stats);
            update_progress_bars(current_game_stats)
        } catch (err) {
            console.log("Error while computing next game turn's variables:", err);
        }
    }
}

async function update_new_game_stats(stats) {
    let game_turn = document.querySelector("#game-turn")
    let game_money = document.querySelector("#game-money")
    let game_inf_airports = document.querySelector("#game-inf-airports");
    game_turn.innerText = stats.game_turn;
    game_money.innerText = stats.money;
    game_inf_airports.innerText = 3; // NEED UPDATES - weird sql i don't wanna touch it
}

async function update_progress_bars(stats) {
    const dis_progress = document.querySelector("#dis-progress");
    dis_progress.style.width = stats.public_dissatisfaction + '%';

    const cure_progress = document.querySelector("#cure-progress");
    cure_progress.style.width = stats.research_progress + '%';

    const inf_progress = document.querySelector("#inf-progress");
    inf_progress.style.width = stats.infected_population + '%';
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
    console.log(game_data[0]);
    let game_turn = document.querySelector("#game-turn")
    let game_money = document.querySelector("#game-money")
    let game_inf_airports = document.querySelector("#game-inf-airports");
    game_turn.innerText = game_data[0].game_turn;
    game_money.innerText = game_data[0].money;
    game_inf_airports.innerText = 3;
    await makeChoice(); // Choices phase
    await next_turn();
}

gameLoop();

async function start_game() {
    while(1===1) {
        await gameLoop();
    }
}

/* 
story / dev commentary or something (just a feature)
story()
while(1 === 1) {
    gameLoop();
}
*/