import os
from unittest import TestCase

from cah.card import Card
from cah.cardtype import CardType
from cah.deck import Deck
from cah.deckmanager import DeckManager


class TestDeckManager(TestCase):

    def setUp(self):
        prompt_card = Card(type=CardType.PROMPT, content="Why did the chicken cross the road?", pick=1)
        response_card1 = Card(type=CardType.RESPONSE, content="A homoerotic subplot")
        response_card2 = Card(type=CardType.RESPONSE, content="To get to the other side")
        card_list = [prompt_card, response_card1, response_card2]
        self.deck = Deck(name="Animals", description="The animal pack", cards=card_list)
        self.manager = DeckManager()

    def test_save(self):
        self.manager.save(self.deck)
        self.assertTrue(os.path.exists(str(self.deck.name) + ".json"))

    def test_load(self):
        self.manager.save(self.deck)
        deck = self.manager.load(uri=str(self.deck.name) + ".json")
        self.assertTrue(isinstance(deck, Deck))

    def tearDown(self):
        try:
            os.remove(str(self.deck.name) + ".json")
        except FileNotFoundError:
            pass
