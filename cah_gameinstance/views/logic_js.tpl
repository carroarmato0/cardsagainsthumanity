let deckapi = {{ !deckapi_uri }};
let websocket_endpoint = {{ !websocket_uri }};
let username;
let game_phase;
let amount_of_players = 0;

// Create WebSocket connection.
let socket = new WebSocket(websocket_endpoint);

function set_cookie(data) {
    console.log("= Storing the server cookie =");
    let d = new Date();
    let expiration_days = 1;
    d.setTime(d.getTime() + (expiration_days*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = "instance_id=" + data.instance_id + "; SameSite=Strict; " + expires;
    document.cookie = "player_id=" + data.player_id + "; SameSite=Strict; " + expires;
}

function get_cookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function identify_player(data) {
    let cookie_instance_id = get_cookie('instance_id');
    let cookie_player_id = get_cookie('player_id');
    let cookie_player_nickname = get_cookie('username');

    // If Instance ID doesn't match or we don't even have a player_id, server will not know us.
    if (cookie_instance_id !== data.instance_id || !cookie_player_id ) {
        //console.log('= Presenting as New Player =');
        //socket.send('{ "event": "new_player", "username": "' + cookie_player_nickname + '" }');
    } else {
        console.log('= Attempting to rejoin =');
        username = cookie_player_nickname;
        socket.send('{ "event": "existing_player", "player_id": "' + cookie_player_id + '" }');
    }
}

function updatePlayerList(players) {
    let players_overview = document.getElementById("players_overview");
    // Clear out any previous content
    players_overview.innerHTML = "";
    let player_list = document.createElement("ul");
    player_list.classList.add("list-group");
    let players_array = eval(players);
    amount_of_players = 0;
    for (var key in players_array) {
        let player_element = document.createElement("li");
        player_element.classList.add("list-group-item");
        player_element.classList.add("d-flex");
        player_element.classList.add("justify-content-between");
        player_element.classList.add("align-items-center");
        player_element.innerHTML = key + (players_array[key].isAdmin ? "<b>Admin</b>" : "") + "<span class=\"badge bg-primary rounded-pill\">" + players_array[key].points + "</span>";
        player_list.appendChild(player_element);
        amount_of_players++;
    }
    players_overview.appendChild(player_list);
}

function evaluateIfGameCanStart() {
    console.log("= Evaluating start game preconditions =");
    let game_start_btn = document.getElementById("game_start_btn");
    let available_decks = document.getElementsByName("decks");
    let selected_decks = [];
    for (var i = 0; i < available_decks.length; i++) {
        if (available_decks[i].checked) {
            selected_decks.push(available_decks[i]);
        }
    }

    if (selected_decks.length > 0 && amount_of_players > 1) {
        game_start_btn.disabled = false;
        game_start_btn.classList.remove('btn-secondary');
        game_start_btn.classList.add('btn-success');
    } else {
        game_start_btn.disabled = true;
        game_start_btn.classList.add('btn-secondary');
        game_start_btn.classList.remove('btn-success');
    }
}

function displayGameSetup(state, isAdmin) {
    // Hide the sign-in
    let signin_div = document.getElementById("sign-in");
    signin_div.style.display = "none";

    // Fetch the Game setup
    let game_setup_div = document.getElementById("game_setup");
    game_setup_div.style.display = "";
    let deck_selection_div = document.getElementById("deck_selection");
    let game_controls = document.getElementById("game_controls");

    if (isAdmin) {
        game_controls.style.display = "";

        // Fetch available decks from DeckAPI
        console.log("= Fetching Available Decks =");
        fetch(deckapi + '/decks/')
          .then(response => response.json())
          .then(function(data) {
            if (Object.keys(data).length > 0) {
                console.log("Found " + data.length + " decks");
                deck_selection_div.innerHTML = '';
                data.forEach(function(deck) {
                    let input_group = document.createElement('div');
                    input_group.classList.add('input-group');
                    input_group.classList.add('mb-3');
                    let input_group_text = document.createElement('div');
                    input_group_text.classList.add('input-group-text');
                    let input_checkbox = document.createElement('input');
                    input_checkbox.classList.add('form-check-input');
                    input_checkbox.setAttribute('type', 'checkbox');
                    input_checkbox.setAttribute('name', 'decks');
                    input_checkbox.addEventListener('change', function(event) {
                        evaluateIfGameCanStart();
                    });

                    let deck_label = document.createElement('label');
                    deck_label.classList.add('form-control');
                    deck_label.innerHTML = deck['name'];
                    input_group_text.appendChild(input_checkbox);
                    input_group.appendChild(input_group_text);
                    input_group.appendChild(deck_label);

                    deck_selection_div.appendChild(input_group);
                });
            } else {
                console.log("No decks found!");
                deck_selection_div.innerHTML = '<div class="alert alert-danger" role="alert">No decks where found!</div>';
            }

        });

    } else {
      deck_selection_div.innerHTML = '<div class="alert alert-info" role="alert">Waiting for game to start.</div>';
    }

}

function process_gamestate(state) {
    console.log("= Processing Game State =");
    if (state.game_phase === "setup") {
        game_phase = "setup";
        if (state.players[username].isAdmin) {
            console.log("= Game Setup Mode, we are the Admin =");
            displayGameSetup(state, true);
        } else {
            console.log("= Game Setup Mode =");
            displayGameSetup(state, false);
        }
    }

    updatePlayerList(state.players);
}

// Connection opened
socket.addEventListener('open', function (event) {
    console.log("= Connected with Server =");
});

// Connection closed
socket.addEventListener('close', function (event) {
    console.log("= Disconnected from Server =");
    setTimeout(function() {
      socket = new WebSocket('ws://localhost:8081/ws');
    }, 1000);
});

// Listen for messages
socket.addEventListener('message', function (event) {
    let response = JSON.parse(event.data);
    console.log(response);

    switch(response.event) {
        case "player_creation":
            set_cookie(response);
            break;
        case "identity_request":
            identify_player(response);
            break;
        case "rejoin_ack":
            console.log("= Rejoined =");
        case "username_ok":
            let signin_error = document.querySelector("#sign-in .invalid-feedback");
            signin_error.style.display = "none";
            signin_error.innerHTML = "";
            break;
        case "username_nok":
            let signin_error_obj = document.querySelector("#sign-in .invalid-feedback");
            signin_error_obj.style.display = "";
            signin_error_obj.innerHTML = "Username not accepted, please enter another.";
            break;
        case "state":
            process_gamestate(response);
            break;
    }
});

// Sign in dialog
let signin_btn = document.getElementById("signin_btn");
signin_btn.addEventListener('click', function (event) {
    username = document.getElementById("nickname_input").value.trim();
    let signin_error = document.querySelector("#sign-in .invalid-feedback");
    if (username === "") {
        signin_error.innerHTML = "Please choose a username."
        signin_error.style.display = "";
    } else {
        document.cookie = "username=" + username + "; SameSite=Strict;";
        console.log("= Sending username: \"" + username +"\" =");
        socket.send('{ "event": "set_username", "username": "' + username + '" }');
    }
});