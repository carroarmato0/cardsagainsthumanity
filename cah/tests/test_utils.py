from unittest import TestCase

from cah.card import Card
from cah.utils import uri_validator, convert_to_dict, dict_to_obj


class TestUtils(TestCase):
    def test_uri_validator(self):
        uri1 = '/data/index.htlm'
        uri2 = 'google.com'
        uri3 = 'http://google.com/'
        uri4 = 'https://google'
        uri5 = 'https://some-api.com/api/give-me-the-deck/12345/'
        self.assertFalse(uri_validator(uri1))
        self.assertFalse(uri_validator(uri2))
        self.assertTrue(uri_validator(uri3))
        self.assertFalse(uri_validator(uri4))
        self.assertTrue(uri_validator(uri5))

    def test_convert_to_dict(self):
        card = Card(type="black", content="Why did the chicken cross the road?", pick=1)
        reference_dict = {
            '__class__': type(card).__name__,
            '__module__': card.__module__,
            'type': 'black',
            'content': 'Why did the chicken cross the road?',
            'pick': 1
        }
        card_dict = convert_to_dict(card)
        self.assertTrue(isinstance(card_dict, dict))
        self.assertDictEqual(card_dict, reference_dict)

    def test_dict_to_obj(self):
        reference_card = Card(type="black", content="Why did the chicken cross the road?", pick=1)
        card_dict = {
            '__class__': type(reference_card).__name__,
            '__module__': reference_card.__module__,
            'type': 'black',
            'content': 'Why did the chicken cross the road?',
            'pick': 1
        }
        card = dict_to_obj(card_dict)
        self.assertEqual(card, reference_card)

