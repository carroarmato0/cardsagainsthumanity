<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title or 'DeckManager'}}</title>
    % for stylesheet in stylesheets:
    {{!stylesheet}}
    % end
    % for script in scripts:
    {{!script}}
    % end
  </head>
  <body>
    <header>
        <h2>DeckManager</h2>
        <p>Welcome to the DeckManager. Here you can create, modify and delete Cards Against Humanity decks of cards.</p>
    </header>
    <nav>
        <a href="/">Overview</a>
    </nav>
    <section id="content">
        {{!base}}
    </section>
    <footer>
        <p>CAH by Christophe Vanlancker &lt;carroarmato0&commat;gmail.com&gt;</p>
    </footer>

  </body>
</html>