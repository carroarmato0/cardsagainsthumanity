<!DOCTYPE html>
<html lang="en">
  <head>
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