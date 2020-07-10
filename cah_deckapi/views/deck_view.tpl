% rebase('base.tpl', title="CAH - DeckManager", stylesheets=stylesheets, scripts=scripts)

    %if deck == None:
    <main class="error"
        <p>Sorry, the deck could not be found.</p>
    </main>
    %else:
    <section>
        <h2>{{ deck['name'] }}</h2>
        <p>Language: {{ deck['lang'] }}</p>
        % if deck['description'].strip() != "":
            <p>Description: {{ deck['description'] }}</p>
         % end
    </section>

    <hr />
    <section id="controls">
        <form action="/api/v1/decks/{{ deck['_id'] }}" method="post">
            <label for="ftype">Type:</label>
            <input type="radio" id="fprompt" name="ftype" value="prompt" checked>
            <label for="fprompt">Prompt</label>
            <input type="radio" id="fresponse" name="ftype" value="response">
            <label for="fanswer">Response</label>
            <label for="fcontent">Content:</label>
            <input type="text" id="fcontent" name="fcontent" value="">
            <label for="fpick">Pick:</label>
            <input type="number" id="fpick" name="fpick" size="1" value="1">
            <label for="fdraw">Draw:</label>
            <input type="number" id="fdraw" name="fdraw" size="1" value="1">
            <input type="submit" value="Add" />
        </form>
    </section>
    <hr />

    <main id="app">
        <ul class="cards">
        % for card in deck['cards']:
            <li class="card {{ card['type'] }}-card">
                <article>
                    <p class="content">{{ card['content'] }}</p>
                    <ul class="modifiers">
                    % if card['type'] == "prompt" and card['pick'] > 1:
                        <li>Pick: {{ card['pick'] }}</li>
                    % end
                    % if card['type'] == "prompt" and card['draw'] > 1:
                        <li>Draw: {{ card['draw'] }}</li>
                    % end
                    </ul>
                </article>
            </li>
        %end
        </ul>
    </main>

    %end
