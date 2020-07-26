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

                // Perform an initial state check of the radio buttons
                if (document.getElementById("fprompt").checked) {
                    document.getElementById('fpick').disabled = false;
                    document.getElementById('fdraw').disabled = false;
                } else if (document.getElementById("fresponse").checked) {
                    document.getElementById('fpick').disabled = true;
                    document.getElementById('fdraw').disabled = true;
                }

                // Perform an initial state check of the content
                document.getElementById("fcontent").value = "";

                // Perform an initial state check of Pick and Draw
                if (document.getElementById("fprompt").checked) {
                    if (document.getElementById('fpick').value <= 0) {
                        document.getElementById('fpick').value = 1;
                    }
                    if (document.getElementById('fdraw').value <= 0) {
                        document.getElementById('fdraw').value = 1;
                    }
                } else if (document.getElementById("fdraw").checked) {
                    if (document.getElementById('fpick').value > 0) {
                        document.getElementById('fpick').value = 0;
                    }
                    if (document.getElementById('fdraw').value > 0) {
                        document.getElementById('fdraw').value = 0;
                    }
                }
                // Add events to radio buttons
                document.getElementById("fprompt").addEventListener('change', function(event) {
                    document.getElementById('fpick').disabled = false;
                    document.getElementById('fdraw').disabled = false;
                    if (document.getElementById('fpick').value <= 0) {
                        document.getElementById('fpick').value = 1;
                    }
                    if (document.getElementById('fdraw').value <= 0) {
                        document.getElementById('fdraw').value = 1;
                    }
                });
                document.getElementById("fresponse").addEventListener('change', function(event) {
                    document.getElementById('fpick').disabled = true;
                    document.getElementById('fdraw').disabled = true;
                    if (document.getElementById('fpick').value > 0) {
                        document.getElementById('fpick').value = 0;
                    }
                    if (document.getElementById('fdraw').value > 0) {
                        document.getElementById('fdraw').value = 0;
                    }
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
                            if (card.pick != 1 && card.draw != 1) {
                                // These are the defaults, so not necessary to show
                                modifiers_cell.innerText = "Pick: " + card.pick + " Draw: " + card.draw;
                            }
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
            if (Object.keys(data).length > 0) {
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

        // Get the Card Submission form
        let card_submit_form = document.querySelectorAll('#card_submit.needs-validation')[0]
        let delete_deck_btn = document.getElementById('delete_deck_btn');
        let card_content_input = document.getElementById('fcontent');
        let card_pick_input = document.getElementById('fpick');
        let card_draw_input = document.getElementById('fdraw');
        let card_promp_radio = document.getElementById('fprompt');
        let card_submit_btn = document.getElementById('add_card_btn');

        card_content_input.addEventListener('keydown', function(event){
            if (card_promp_radio.checked) {
                let regex = /(?<=(\$|\s))(_+)(?!\w)/gm;
                let occurrences = (card_content_input.value.match(regex) || []).length;
                if (occurrences > 1) {
                    card_pick_input.value = occurrences;
                    card_draw_input.value = occurrences;
                } else {
                    card_pick_input.value = 1;
                    card_draw_input.value = 1;
                }
            }
        });

        if (card_submit_form) {
            card_submit_form.addEventListener('submit', function (event) {
                if (!card_submit_form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                else {
                    console.log("= Submitting Card = ");
                    event.preventDefault()
                    event.stopPropagation()

                    let card_type = "";

                    if (document.getElementById('fprompt').checked) {
                        card_type = "prompt"
                    } else if (document.getElementById('fresponse').checked) {
                        card_type = "response"
                    }

                    let card_content = document.getElementById("fcontent").value;
                    let card_pick = document.getElementById("fpick").value;
                    let card_draw = document.getElementById("fdraw").value;

                    let card_json = JSON.stringify(
                        { 'type': card_type,
                          'content': card_content,
                          'pick': card_pick,
                          'draw': card_draw
                         })

                    fetch('/api/v1/decks/' + deck_id, {
                        method: 'post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: card_json
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status == "ok") {
                            // Reset validation of card submit form
                            card_submit_form.classList.remove('was-validated');
                            card_submit_form.classList.add('needs-validation');
                            fetchDeck(card_overview, deck_id);
                        }
                    });
                }

                card_submit_form.classList.add('was-validated');
            });

            card_submit_form.addEventListener('keyup' ,function(event){
                if (event.code === 'Enter') {
                    event.preventDefault();
                    card_submit_btn.click();
                }
            })

            delete_deck_btn.addEventListener('click', function(event) {
                if (confirm('Are you sure you want to delete this deck?')) {
                    console.log('Deleting Deck: ' + deck_id);

                    fetch('/api/v1/decks/' + deck_id, {
                        method: 'delete',
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status == "ok") {
                            window.location.replace('/');
                        } else {
                            console.log('An error occurred deleting the deck')
                        }
                    });
                }
            });
        }

    }

    let export_import_form = document.getElementById('import_export_submit');
    if (export_import_form) {
        export_import_form.addEventListener('submit', function (event) {
            if (!export_import_form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            else {
                event.preventDefault()
                event.stopPropagation()

                import_input = document.getElementById('import_input')

                fetch('/api/v1/decks/import', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: import_input.files[0]
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status == "ok") {
                        console.log('Import successful')
                        // Reset validation of card submit form
                        export_import_form.classList.remove('was-validated');
                        export_import_form.classList.add('needs-validation');
                        export_import_form.reset();
                        fetchDecks(deck_overview);
                    } else {
                        console.log('Import failed')
                    }
                });

            }
        })
    }

})