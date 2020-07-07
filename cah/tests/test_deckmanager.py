import os
from unittest import TestCase

from cah.card import Card
from cah.deck import Deck
from cah.deckmanager import DeckManager


class TestDeckManager(TestCase):

    def setUp(self):
        black_card = Card(type="black", content="Why did the chicken cross the road?", pick=1)
        white_card1 = Card(type="white", content="A homoerotic subplot")
        white_card2 = Card(type="white", content="To get to the other side")
        card_list = [black_card, white_card1, white_card2]
        self.deck = Deck(id=0, name="Animals", description="The animal pack", cards=card_list)
        self.manager = DeckManager()

    def test_save(self):
        self.manager.save(self.deck)
        self.assertTrue(os.path.exists(str(self.deck.id) + ".json"))

    def test_load(self):
        self.manager.save(self.deck)
        deck = self.manager.load(uri=str(self.deck.id) + ".json")
        self.assertTrue(isinstance(deck, Deck))

    def tearDown(self):
        try:
            os.remove(str(self.deck.id) + ".json")
        except FileNotFoundError:
            pass
