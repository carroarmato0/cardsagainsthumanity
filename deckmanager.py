import urllib.request
import json

from deck import Deck
from utils import convert_to_dict, dict_to_obj


class DeckManager:
    """ This library helps loading and writing card Decks """

    def load(self, uri=None):
        """ Load a json encoded deck from a URL or path """
        deck = None

        if uri is None:
            raise ValueError(f"Empty uri has been given to load a deck")
        else:
            """ Attempt to load the json data as a url """
            try:
                with urllib.request.urlopen(uri) as url:
                    data = json.loads(url.read().decode())
                    deck = json.loads(data, object_hook=dict_to_obj)
            except ValueError:
                try:
                    """ Attempt to load the json data as a file """
                    with open(uri, 'r') as reader:
                        deck = json.loads(reader.read(), object_hook=dict_to_obj)
                except FileNotFoundError:
                    pass
        return deck

    def save(self, deck=None):
        """ Save a Deck of cards to the filesystem """
        if not isinstance(deck, Deck):
            raise ValueError(f"The supplied deck is not recognized")
        else:
            """
            deck_json = DeckEncoder().encode(deck)
            """
            deck_json = json.dumps(deck, default=convert_to_dict, indent=4, sort_keys=True)
            with open(str(deck.id) + '.json', 'w', encoding="utf-8") as writer:
                writer.write(deck_json)
