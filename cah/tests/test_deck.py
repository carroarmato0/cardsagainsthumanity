from unittest import TestCase
from cah.card import Card
from cah.deck import Deck


class TestDeck(TestCase):

    def setUp(self):
        black_card = Card(type="black", content="Why did the chicken cross the road?", answer_count=1)
        white_card1 = Card(type="white", content="A homoerotic subplot")
        white_card2 = Card(type="white", content="To get to the other side")
        card_list = [black_card, white_card1, white_card2]
        self.deck = Deck(id=0, name="Animals", description="The animal pack", cards=card_list)

    def test_black_cards(self):
        self.assertEqual(len(self.deck.black_cards), 1)

    def test_white_cards(self):
        self.assertEqual(len(self.deck.white_cards), 2)

    def test_id(self):
        self.assertEqual(self.deck.id, 0)

    def test_name(self):
        self.assertEqual(self.deck.name, "Animals")

    def test_description(self):
        self.assertEqual(self.deck.description, "The animal pack")

    def test_len(self):
        self.assertEqual(self.deck.len, 3)

    def test_eq(self):
        black_card = Card(type="black", content="Why did the chicken cross the road?", answer_count=1)
        white_card1 = Card(type="white", content="A homoerotic subplot")
        white_card2 = Card(type="white", content="To get to the other side")
        card_list_a = [black_card, white_card1, white_card2]
        deck_a = Deck(id=0, name="Animals", description="The animal pack", cards=card_list_a)

        deck_b = Deck(id=0, name="Animals", description="The animal pack", cards=[])

        self.assertEqual(self.deck, deck_a)
        self.assertNotEqual(self.deck, deck_b)
