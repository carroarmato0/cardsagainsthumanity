function fetchDeck(table, id) {
    console.log("= Fetching Deck " + id + " =")
    fetch('/api/v1/decks/' + id)
      .then(response => response.json())
      .then(function(data) {
            if (data) {
                // Hide the No Deck message
                document.getElementById("no_deck").style.display='none';
                //Reveal the Cards table
                document.getElementById("deck_container").style.display='';
                // Set Deck metadata
                document.getElementById("deck_name").innerText=data.name;
                document.getElementById("deck_language").innerText="Language: " + data.lang;
                document.getElementById("deck_description").innerText="Description: " + data.description;

                // Add events to radio buttons
                document.getElementById("fprompt").addEventListener('onclick', function(event) {
                    console.log("Prompt clicked");
                });
                document.getElementById("fanswer").addEventListener('onclick', function(event) {
                    console.log("Answer clicked");
                });

                // Check if Deck has cards
                if (data.cards.length > 0) {
                    // Hide no cards message
                    document.getElementById("no_cards").style.display='none';
                    // Get tbody of table
                    let tbody = table.getElementsByTagName('tbody')[0]
                    // Wipe Deck table body
                    tbody.innerHTML = ""
                    // Reveal the Card table
                    table.style.display='';
                    // Loop through the cards and add elements
                    data.cards.forEach(function(card) {
                        //console.log(card);
                        let row = tbody.insertRow();
                        let type_cell = row.insertCell();
                        type_cell.classList.add('align-middle');
                        type_cell.innerText = card.type;
                        let content_cell = row.insertCell();
                        content_cell.classList.add('align-middle');
                        content_cell.innerText = card.content;
                        let modifiers_cell = row.insertCell();
                        if (card.type == "prompt") {
                            row.classList.add('table-dark');
                            modifiers_cell.innerText = "Pick: " + card.pick + " Draw: " + card.draw;
                        } else {
                            row.classList.add('table-light');
                        }
                        modifiers_cell.classList.add('align-middle');
                        let action_cell = row.insertCell();

                        let action_cell_btn_toolbar = document.createElement('div');
                        action_cell_btn_toolbar.classList.add('btn-toolbar');

                        let action_cell_btn_group1 = document.createElement('div');
                        action_cell_btn_group1.classList.add('btn-group');
                        action_cell_btn_group1.classList.add('mr-2');

                        let edit_button = document.createElement('button');
                        edit_button.innerText="Edit";
                        edit_button.classList.add('btn');
                        edit_button.classList.add('btn-warning');
                        action_cell_btn_group1.append(edit_button);

                        let action_cell_btn_group2 = document.createElement('div');
                        action_cell_btn_group2.classList.add('btn-group');

                        let delete_button = document.createElement('button');
                        delete_button.innerText="Delete";
                        delete_button.classList.add('btn');
                        delete_button.classList.add('btn-danger');
                        action_cell_btn_group2.append(delete_button);

                        action_cell_btn_toolbar.append(action_cell_btn_group1);
                        action_cell_btn_toolbar.append(action_cell_btn_group2);
                        action_cell.append(action_cell_btn_toolbar);
                     });
                 } else {
                    // Show no cards message
                    document.getElementById("no_cards").style.display='';
                 }
            } else {
                // Show the No Deck message
                document.getElementById("no_deck").style.display='';
                // Hide the Cards table
                document.getElementById("deck_container").style.display='none';
            }

       });
};

function fetchDecks(table) {
    console.log("= Fetching Decks = ")
    fetch('/api/v1/decks/')
      .then(response => response.json())
      .then(function(data) {
            if (data.length > 0) {
                console.log("Found " + data.length + " decks");
                // Hide the No Deck message
                document.getElementById("no_decks").style.display='none';
                // Get tbody of table
                let tbody = table.getElementsByTagName('tbody')[0]
                // Wipe Deck table body
                tbody.innerHTML = ""
                // Reveal the Deck table
                table.style.display='';
                // Loop through the decks and add elements
                data.forEach(function(deck) {
                    //console.log(deck);
                    let row = tbody.insertRow();
                    let id_cell = row.insertCell();
                    let id_link = document.createElement('a');
                    id_link.setAttribute('href', '/decks/' + deck._id["$oid"]);
                    id_link.innerText = deck._id["$oid"];
                    id_cell.append(id_link);
                    let name_cell = row.insertCell();
                    name_cell.innerText = deck.name;
                    let description_cell = row.insertCell();
                    description_cell.innerText = deck.description;
                    let language_cell = row.insertCell();
                    language_cell.innerText = deck.lang;
                    let card_count_cell = row.insertCell();
                    card_count_cell.innerText = deck.cards.length;
                 });
            }
       });
};

// Add events on DOM loaded
document.addEventListener('DOMContentLoaded', function(event) {
    // Try getting a deck_overview
    let deck_overview = document.getElementById("deck_overview")
    if (deck_overview) {
        fetchDecks(deck_overview);
    }

    // Try getting the deck submission form
    let deck_submit_form = document.querySelectorAll('#deck_submit.needs-validation')[0]
    if (deck_submit_form) {
        deck_submit_form.addEventListener('submit', function (event) {
            if (!deck_submit_form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            } else {
                console.log("= Submitting Deck = ");
                event.preventDefault()
                event.stopPropagation()

                deck_name = document.getElementById('fname').value
                deck_description = document.getElementById('fdescription').value
                deck_lang = document.getElementById('flang').value

                fetch('/api/v1/decks/', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(
                        { 'name': deck_name,
                          'description': deck_description,
                          'lang': deck_lang,
                          'cards': []
                         })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status == "ok") {
                        window.location.replace("/decks/" + data.id);
                    }
                });
            }

            deck_submit_form.classList.add('was-validated')
          }, false)
    }

    // Try getting a card_overview
    let card_overview = document.getElementById("card_overview")
    if (card_overview) {
        // Get ID
        let deck_id = card_overview.dataset.id
        fetchDeck(card_overview, deck_id);
    }

})