<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Cah</title>
    <meta charset="utf-8">
    <link rel="apple-touch-icon" sizes="57x57" href="/favicon/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/favicon/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/favicon/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/favicon/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/favicon/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/favicon/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/favicon/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/favicon/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="/favicon/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
    <link rel="manifest" href="/favicon/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="/favicon/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css">
  </head>
  <body>

    <div id="app" class="container mt-5">

        <div id="sign-in">
            <div class="mb-3">
                <input type="text" class="form-control" id="nickname_input" required placeholder="username">
                <div class="invalid-feedback">Please choose a username.</div>
            </div>
            <div class="invalid-feedback">
                I can't let you do that John.
            </div>
            <div class="mb-3">
                <button class="btn btn-primary mb-3" type="button" id="signin_btn">Sign In</button>
            </div>
        </div>

        <div id="game_setup" class="container" style="display: none;">
            <div class="row">
                <div id="deck_selection">
                    <span>Deck Selection comes here</span>
                </div>
            </div>
            <div class="row">
                <div id="game_controls">
                    <button id="game_start_btn" class="btn btn-secondary mb-3 form-control" disabled>Start Game</button>
                </div>
            </div>
            <div class="row">
                <div id="players_overview" class="col">
                    <span>Players appear here</span>
                </div>
                <div id="messages" class="col">
                    <span>Messages appear here</span>
                </div>
            </div>
        </div>

    </div>

    <script src="/js/main.js"></script>

  </body>
</html>