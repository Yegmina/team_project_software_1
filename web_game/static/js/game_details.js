'use strict';

async function show_game_details() {
    const stats = document.querySelector("#stats-table");
    let div = document.querySelector("#game_details");
    const game_data = await JSON.parse(div.innerHTML);
    console.log(game_data)
    for (const [key, value] of Object.entries(game_data)) {
        let row = document.createElement('tr');
        let name = document.createElement('th');
        let data = document.createElement('th');
        let key_string = "";
        for (let i = 0; i < key.length; i++) {
            if (key[i] === '_') key_string = key_string + ' ';
            else key_string = key_string + key[i];
        }
        key_string = key_string.charAt(0).toUpperCase() + key_string.slice(1);
        name.innerHTML = `${key_string}`;
        data.innerHTML = value;

        row.appendChild(name);
        row.appendChild(data);

        stats.appendChild(row);
    }
    document.querySelector("#game_table").removeChild(div);

    let continue_game = document.querySelector("#continue");
    continue_game.href = `/play/${game_data.id}`;
}
show_game_details();