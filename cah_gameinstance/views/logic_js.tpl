let deckapi = '{{ !deckapi_uri }}';
let websocket_endpoint = '{{ !websocket_uri }}';
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

// Update the players list
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

// Verify if all the conditions are met to be able to start the game
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
        return true;
    } else {
        game_start_btn.disabled = true;
        game_start_btn.classList.add('btn-secondary');
        game_start_btn.classList.remove('btn-success');
        return false;
    }

    return false;
}

// Allow the game admin to configure the instance
function displayGameSetup(state, isAdmin) {
    // Hide the sign-in
    show_sign_in(false);

    // Fetch the Game setup
    show_game_setup(true);
    let game_setup_div = document.getElementById("game_setup");
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
                    input_checkbox.setAttribute('data-id', deck['_id']['$oid']);
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

        let start_game_btn = document.getElementById("game_start_btn");
        start_game_btn.addEventListener("click", function(event) {
            if (evaluateIfGameCanStart) {
                // Get IDs of checked decks
                let checked_deck_checkboxes = document.querySelectorAll('#deck_selection input[type="checkbox"]:checked');
                let chosen_deck_ids = [];
                for (var checkbox of checked_deck_checkboxes) {
                    chosen_deck_ids.push("\"" + checkbox.dataset.id + "\"");
                }
                console.log("= Requesting Server to Start Game =");
                socket.send('{ "event": "game_start", "deck_ids": [' + chosen_deck_ids.join() + '] }');
            }
        });

    } else {
      deck_selection_div.innerHTML = '<div class="alert alert-info" role="alert">Waiting for game to start.</div>';
    }

}

function show_sign_in(isTrue) {
    let signin_div = document.getElementById("sign-in");
    if (isTrue) {
        signin_div.style.display = "";
    }
    else {
        signin_div.style.display = "none";
    }
}

function show_game_setup(isTrue) {
    let game_setup_div = document.getElementById("game_setup");
    if (isTrue) {
        game_setup_div.style.display = "";
    }
    else {
        game_setup_div.style.display = "none";
    }
}

function show_game_board(isTrue) {
    let game_board_div = document.getElementById("game_board");
    if (isTrue) {
        game_board_div.style.display = "";
    }
    else {
        game_board_div.style.display = "none";
    }
}

function show_game_dashboard(isTrue) {
    let game_dashboard_div = document.getElementById("game_dashboard");
    if (isTrue) {
        game_dashboard_div.style.display = "";
    }
    else {
        game_dashboard_div.style.display = "none";
    }
}

function areWeCzar(state) {
    return state['players'][username].isCzar;
}

function render_cards(state) {
    // Render Cards on Deck
    let cards_on_deck_div = document.getElementById("cards_on_deck");
    // Reset content
    cards_on_deck_div.innerHTML = "";

    let cards_on_deck_list = document.createElement('ul');
    cards_on_deck_list.classList.add("cards");

    //Render the Prompt Card
    let prompt_card_list_element = document.createElement('li');
    prompt_card_list_element.classList.add("card");
    prompt_card_list_element.classList.add( state['prompt_card']['type'] + "-card" );
    let prompt_card_article = document.createElement('article');
    let prompt_card_content = document.createElement('p');
    prompt_card_content.classList.add('content');
    prompt_card_content.textContent = state['prompt_card']['content'];
    let prompt_card_modifiers = document.createElement('ul');
    prompt_card_modifiers.classList.add('modifiers');
    if ( state['prompt_card']['type'] === "prompt" && state['prompt_card']['pick'] > 1 ) {
        let prompt_card_pick = document.createElement('li');
        prompt_card_pick.textContent = "Pick: " + state['prompt_card']['pick'];
        prompt_card_modifiers.appendChild(prompt_card_pick);
    }
    if (state['prompt_card']['type'] === "prompt" && state['prompt_card']['draw'] > 1) {
        let prompt_card_draw = document.createElement('li');
        prompt_card_draw.textContent = "Draw: " + state['prompt_card']['draw'];
        prompt_card_modifiers.appendChild(prompt_card_draw);
    }
    prompt_card_article.appendChild(prompt_card_content);
    prompt_card_article.appendChild(prompt_card_modifiers);
    prompt_card_list_element.appendChild(prompt_card_article);
    cards_on_deck_list.appendChild(prompt_card_list_element);
    cards_on_deck.appendChild(cards_on_deck_list);

    // Render my response cards
    let my_cards_div = document.getElementById("my_cards");
    // Reset content
    my_cards_div.innerHTML = "";

    let my_cards_list = document.createElement('ul');
    my_cards_list.classList.add("cards");

    state['my_cards'].forEach(function(card){
        let response_card_list_element = document.createElement('li');
        response_card_list_element.setAttribute('data-type', card['type']);
        response_card_list_element.setAttribute('data-content', card['content']);
        response_card_list_element.classList.add("card");
        response_card_list_element.classList.add( card['type'] + "-card" );
        // If we are the current Czar, disable our deck selection
        if (areWeCzar(state)) {
            response_card_list_element.classList.add("disabled");
        } else {
            response_card_list_element.addEventListener('click', function(event) {
                // Get card information
                let card_obj = event.target;

                // Check if toggling is necessary
                if (card_obj.classList.contains('selected')) {
                    card_obj.classList.remove('selected');
                } else {
                    card_obj.classList.add('selected');
                }

                // Only submit cards if the amount of selected ones satisfies the prompt card pick number
                let selected_cards = document.querySelectorAll("#my_cards .selected");
                if ( selected_cards.length >= state['prompt_card']['pick'] ) {
                    console.log("= Sending our selected cards to server =")
                }

            });
        }
        let response_card_article = document.createElement('article');
        let response_card_content = document.createElement('p');
        response_card_content.classList.add('content');
        response_card_content.textContent = card['content'];
        response_card_article.appendChild(response_card_content);
        response_card_list_element.appendChild(response_card_article);
        my_cards_list.appendChild(response_card_list_element);
    })
    my_cards_div.appendChild(my_cards_list);
}

// Process the game state sent by the server
function process_gamestate(state) {
    console.log("= Processing Game State =");
    show_sign_in(false);
    show_game_dashboard(true);

    if (state.game_phase === "setup") {
        game_phase = "setup";
        if (state.players[username].isAdmin) {
            console.log("= Game Setup Mode, we are the Admin =");
            displayGameSetup(state, true);
        } else {
            console.log("= Game Setup Mode =");
            displayGameSetup(state, false);
        }
    } else if (state.game_phase === "draw") {
        game_phase = "draw"
        console.log("= Game Draw Mode =");
        show_game_setup(false);
        show_game_board(true);
        render_cards(state);
    }

    updatePlayerList(state.players);
}

// Display that a new player has joined the game
function process_player_joined(data) {
    console.log("= Player joined event =");
    let message_input = document.getElementById("messages_input");
    let date = moment.unix(data['timestamp']);
    message_input.textContent += date.format('DD/MM HH:mm:ss z') + " " + data['username'] + " joined.\r\n";
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
        case "player_joined":
            process_player_joined(response);
            break;
    }
});

// Sign in dialog
show_sign_in(true);
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