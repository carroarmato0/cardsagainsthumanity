% rebase('base.tpl', title="CAH - DeckManager", stylesheets=stylesheets, scripts=scripts)

        <hr/>
        <form id="deck_submit" class="row gy-2 gx-3 align-items-center needs-validation" novalidate action="">
            <div class="row g-1">
                <div class="col-auto">
                    <input type="text" class="form-control" id="fname" name="fname" placeholder="Deck Name" aria-label="Deck Name" required>
                    <div class="valid-feedback">
                        Looks good!
                    </div>
                    <div class="invalid-feedback">
                        Please fill in a name.
                    </div>
                </div>
                <div class="col-auto">
                    <input type="text" class="form-control" id="fdescription" name="fdescription" placeholder="Description" aria-label="Description">
                    <div class="valid-feedback">
                        Looks good!
                    </div>
                </div>
                <div class="col-auto">
                    <select class="form-select" id="flang" name="flang" aria-label="Language" required>
                        % for lang in languages:
                            % if lang == "en":
                                <option selected value="{{ lang }}">{{ languages[lang].name }}</option>
                            % elif lang in {'ia'}:
                                % pass;
                            % else:
                                <option value="{{ lang }}">{{ languages[lang].name }}</option>
                            % end
                        % end
                    </select>
                    <div class="valid-feedback">
                        Looks good!
                    </div>
                    <div class="invalid-feedback">
                        Please select a valid language.
                    </div>
                </div>
                <div class="col-auto">
                    <button type="submit" class="btn btn-success">Add</button>
                </div>
            </div>
        </form>
        </br>
        <form id="import_export_submit" class="row gy-2 gx-3 align-items-center action="">
            <div class="row g-1">
                <div class="col-auto">
                    <div class="form-file">
                      <input id="import_input" type="file" class="form-file-input" required>
                      <label class="form-file-label" for="import_input">
                        <span class="form-file-text">Import Deck(s)...</span>
                        <span class="form-file-button">Browse</span>
                      </label>
                    </div>
                </div>
                <div class="col-auto">
                    <button id="import_btn" type="submit" class="btn btn-primary">Import</button>
                </div>
                <div class="col-auto">
                    <a class="btn btn-info" href="/api/v1/decks/export" role="button">Export</a>
                </div>
            </div>
        </form>
        <hr/>

        <div id="no_decks" class="m-5" style="text-align:center;">
            <span class="alert alert-primary">No decks could be found.</span>
        </div>

        <table id="deck_overview" class="table table-hover" style="display: none;">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Description</th>
                    <th scope="col">Language</th>
                    <th scope="col">Cards</th>
                </tr>
            </thead>
            <tbody>
                <tr style="display: none;">
                    <td></td>
                </tr>
            </tbody>
        </table>
