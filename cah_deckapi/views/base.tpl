<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title or 'DeckManager'}}</title>
    <link rel="stylesheet" href="/css/bootstrap/bootstrap.min.css">
    % for stylesheet in stylesheets:
    {{!stylesheet}}
    % end
    <script src="/js/popper.min.js"></script>
    <script src="/js/bootstrap/bootstrap.min.js"></script>
    <script src="/js/main.js"></script>
    % for script in scripts:
    {{!script}}
    % end
  </head>
  <body>
    <header>
        <h2>DeckManager</h2>
        <p>Welcome to the DeckManager. Here you can create, modify and delete Cards Against Humanity decks of cards.</p>
    </header>
    <ul class="nav nav-tabs">
        <li class="nav-item">
            <a class="nav-link active" href="/">Overview</a>
        </li>
    </ul>
    <div class="container-fluid">
        {{!base}}
    </div>
    <footer class="">
        <p>CAH by Christophe Vanlancker &lt;carroarmato0&commat;gmail.com&gt;</p>
    </footer>
  </body>
</html>