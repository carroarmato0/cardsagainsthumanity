from unittest import TestCase
from cah.card import Card


class TestCard(TestCase):
    def setUp(self):
        self.card_black = Card(type="black", content="Why did the chicken cross the road?", answer_count=1)
        self.card_white = Card(type="white", content="A homoerotic subplot", answer_count=0)

    def test_type(self):
        self.assertEqual(self.card_black.type, "black")
        self.assertEqual(self.card_white.type, "white")

    def test_content(self):
        self.assertEqual(self.card_black.content, "Why did the chicken cross the road?")
        self.assertEqual(self.card_white.content, "A homoerotic subplot")

    def test_answer_count(self):
        self.assertEqual(self.card_black.answer_count, 1)
        self.assertEqual(self.card_white.answer_count, 0)

    def test_eq(self):
        card = Card(type="black", content="Why did the chicken cross the road?", answer_count=1)
        self.assertEqual(card, self.card_black)
        self.assertNotEqual(self.card_black, self.card_white)