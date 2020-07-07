from unittest import TestCase
from cah.card import Card
from cah.cardtype import CardType


class TestCard(TestCase):
    def setUp(self):
        self.prompt_card = Card(type=CardType.PROMPT, content="Why did the chicken cross the road?", pick=1)
        self.response_card = Card(type=CardType.RESPONSE, content="A homoerotic subplot", pick=0)

    def test_type(self):
        self.assertEqual(self.prompt_card.type, CardType.PROMPT)
        self.assertEqual(self.response_card.type, CardType.RESPONSE)

    def test_content(self):
        self.assertEqual(self.prompt_card.content, "Why did the chicken cross the road?")
        self.assertEqual(self.response_card.content, "A homoerotic subplot")

    def test_pick(self):
        self.assertEqual(self.prompt_card.pick, 1)
        self.assertEqual(self.response_card.pick, 0)

    def test_draw(self):
        self.assertEqual(self.prompt_card.draw, 1)
        self.assertEqual(self.response_card.draw, 0)

    def test_eq(self):
        card = Card(type=CardType.PROMPT, content="Why did the chicken cross the road?", pick=1)
        self.assertEqual(card, self.prompt_card)
        self.assertNotEqual(self.prompt_card, self.response_card)
