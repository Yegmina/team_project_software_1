'use strict';

const div = document.createElement('div');
const table = document.createElement('table');
const body = document.querySelector('body');

div.className = 'container';
div.style = `
    display: flex;
    flex-direction: column;
    gap: 15px;
`
// div.style = `
table.id = 'stats-table';
table.innerHTML = `        
    <tr>
        <th style="font-size:25px; color:rgb(0, 157, 255)">Attribute</th>
        <th style="font-size:25px; color:rgb(0, 157, 255)">Value</th>
    </tr>
`;


async function show_game(game_id) {
    div.innerHTML = '';
    table.innerHTML = '';
    div.appendChild(table);
    let game_data = await fetch(`/dev/fetch_games/${game_id}`);
    game_data = await game_data.json()
    console.log(game_data);

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

        table.appendChild(row);
    }

    let button = document.createElement('a');
    button.id = 'button';
    button.href = `/play/${game_id}`;
    button.innerText = `Play this game instead`
    div.appendChild(table);
    div.appendChild(button);
    body.appendChild(div);
}


async function player_name_submission() {
    const form = document.querySelector("#name_input");
    form.addEventListener('submit', async (evt) => {
        evt.preventDefault();
        const entered_name = document.querySelector("#name").value;
        let data = await fetch(`/dev/game_exists/${entered_name}`);
        data = await data.json();
        console.log(data[0])
        if (data.length != 0) {
            console.log(data);
            show_game(data[0][0]) // data[0][0] == game_id
        }
        else {
            await fetch(`/new_game`, {
                method: "POST",
                body: JSON.stringify({
                    'name': `${entered_name}`,
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            }).then( (response) => {
                if(response.redirected) {
                    window.location.href = response.url;
                }
            })
        }
    })
}
player_name_submission();