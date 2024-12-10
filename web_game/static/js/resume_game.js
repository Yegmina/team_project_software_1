'use strict';


async function load_game_list() {
    all_games = await response.json()
    console.log(all_games);
    const list = document.querySelector("#game-list");
    list.innerHTML = '';
    for (let game of all_games) {
        let li = document.createElement('li');
        let a = document.createElement('a');
        a.innerText = game[1];
        a.href = `fetch_game/${game[0]}`;
        li.appendChild(a);
        list.appendChild(li);
    }
}
load_game_list();