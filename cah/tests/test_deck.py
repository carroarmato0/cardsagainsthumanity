from unittest import TestCase
from cah.card import Card
from cah.cardtype import CardType
from cah.deck import Deck


class TestDeck(TestCase):

    def setUp(self):
        prompt_card = Card(type=CardType.PROMPT, content="Why did the chicken cross the road?", pick=1)
        response_card1 = Card(type=CardType.RESPONSE, content="A homoerotic subplot")
        response_card2 = Card(type=CardType.RESPONSE, content="To get to the other side")
        card_list = [prompt_card, response_card1, response_card2]
        self.deck = Deck(name="Animals", description="The animal pack", cards=card_list)

    def test_prompt_cards(self):
        self.assertEqual(len(self.deck.prompt_cards), 1)

    def test_response_cards(self):
        self.assertEqual(len(self.deck.response_cards), 2)

    def test_name(self):
        self.assertEqual(self.deck.name, "Animals")

    def test_description(self):
        self.assertEqual(self.deck.description, "The animal pack")

    def test_len(self):
        self.assertEqual(self.deck.len, 3)

    def test_eq(self):
        prompt_card = Card(type=CardType.PROMPT, content="Why did the chicken cross the road?", pick=1)
        response_card1 = Card(type=CardType.RESPONSE, content="A homoerotic subplot")
        response_card2 = Card(type=CardType.RESPONSE, content="To get to the other side")
        card_list_a = [prompt_card, response_card1, response_card2]
        deck_a = Deck(name="Animals", description="The animal pack", cards=card_list_a)

        deck_b = Deck(name="Animals", description="The animal pack", cards=[])

        self.assertEqual(self.deck, deck_a)
        self.assertNotEqual(self.deck, deck_b)

    def test_add_card(self):
        card = Card(type=CardType.RESPONSE, content="A wombat")
        self.deck.add_card(card)
        self.assertIn(card, self.deck.response_cards)

    def test_remove_card(self):
        card = Card(type=CardType.RESPONSE, content="To get to the other side")
        self.deck.remove_card(card)
        self.assertNotIn(card, self.deck.response_cards)

    def test_to_json_obj(self):
        json_obj = self.deck.to_json_obj()
        self.assertTrue(isinstance(json_obj, dict))
        self.assertEqual(json_obj['name'], self.deck.name)
        self.assertEqual(json_obj['description'], self.deck.description)
        self.assertEqual(json_obj['lang'], self.deck.lang)
        for card in self.deck.cards:
            card_obj = card.to_json_obj()
            self.assertIn(card_obj, json_obj['cards'])

    def test_to_json(self):
        json_str = self.deck.to_json()
        self.assertTrue(isinstance(json_str, str))
        self.assertEqual(json_str, '{"name": "Animals", "description": "The animal pack", "lang": "en", "cards": [{'
                                   '"type": "prompt", "content": "Why did the chicken cross the road?", "pick": 1, '
                                   '"draw": 1}, {"type": "response", "content": "A homoerotic subplot", "pick": 0, '
                                   '"draw": 0}, {"type": "response", "content": "To get to the other side", '
                                   '"pick": 0, "draw": 0}]}')
