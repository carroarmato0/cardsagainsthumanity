% rebase('base.tpl', title="CAH - DeckManager", stylesheets=stylesheets, scripts=scripts)

        <div id="no_deck" class="m-5" style="text-align:center;">
            <span class="alert alert-danger">The requested Deck could not be found.</span>
        </div>

        <div id="deck_container" style="display: none;">
            <div id="deck" class="container-fluid">
                <h2 id="deck_name">Deck Name</h2>
                <p id="deck_language">Language</p>
                <p id="deck_description">Description</p>
            </div>

            <hr />
            <form id="card_submit" class="form-inline gy-2 gx-3 align-items-center needs-validation" novalidate action="">
                <div class="row">
                    <div class="col-auto mt-2">
                        <label class="form-label" for="ftype">Type: </label>
                        <input class="form-check-input" type="radio" name="ftype" checked id="fprompt">
                        <label class="form-check-label" for="fprompt">Prompt</label>
                        <input class="form-check-input" type="radio" name="ftype" id="fresponse">
                        <label class="form-check-label" for="fresponse">Response</label>
                    </div>
                    <div class="col-auto">
                        <input class="form-control" type="text" id="fcontent" name="fcontent" required placeholder="Content" />
                        <div class="invalid-feedback">
                            Please fill in the content.
                        </div>
                    </div>
                    <div class="col-auto mt-1">
                        <label class="form-check-label" for="fpick">Pick:</label>
                        <input type="number" id="fpick" name="fpick" size="2" min="0" value="1">

                        <label class="form-check-label" for="fdraw">Draw:</label>
                        <input type="number" id="fdraw" name="fdraw" size="2" min="0" value="1">
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary">Add</button>
                        <button type="submit" class="btn btn-danger">Delete Deck</button>
                    </div>
                </div>
            </form>
            <hr />

            <div id="no_cards" class="m-5" style="text-align:center;">
                <span class="alert alert-primary">This deck has no cards. Add some!</span>
            </div>

            <table id="card_overview" class="table table-hover" data-id="{{ deck_id }}" style="display: none;">
                <thead>
                    <tr>
                        <th scope="col">Type</th>
                        <th scope="col">Content</th>
                        <th scope="col">Modifiers</th>
                        <th scope="col">&nbsp;</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="display: none;">
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
