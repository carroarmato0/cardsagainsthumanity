from cah.card import Card
from cah.cardtype import CardType


class Deck:
    """ A Class representing a deck of cards """

    def __init__(self, name='', description='', cards=[], lang='en'):
        """
        Initializer for the Deck
        :param name: a short title/name for this deck
        :param description: the description for this deck
        :param cards: a list of cards, ideally a combination of black and white types
        :param lang: language code
        """
        if not name:
            raise ValueError(f"Deck name cannot be empty")
        if not isinstance(cards, list):
            raise ValueError(f"Supplied cards is not a list")

        self.name = name
        self.description = description
        self.cards = cards
        self.lang = lang

    @property
    def prompt_cards(self):
        """
        Get all the prompt cards in the deck
        :return: list of prompt cards
        """
        cards = []
        for card in self.cards:
            if card.type == CardType.PROMPT:
                cards.append(card)
        return cards

    @property
    def response_cards(self):
        """
        Get all the response cards in the deck
        :return: list of response cards
        """
        cards = []
        for card in self.cards:
            if card.type == CardType.RESPONSE:
                cards.append(card)
        return cards

    def name(self):
        """
        Return the Name of this deck
        :return: name of this deck
        """
        return self.name

    def description(self):
        """
        Return the Description of this deck
        :return: description of this deck
        """
        return self.description

    def lang(self):
        """
        Return the ISO 639-1 code representation of the main Deck's language
        :return: language code of this deck
        """
        return self.lang

    @property
    def len(self):
        """
        Get the amount of cards in the deck
        :return: the amount of cards in the deck
        """
        return len(self.cards)

    def __eq__(self, other):
        """
        Validate object for equality
        :param other: the other object to compare to
        :return: True of False is the object is equal to this instance
        """
        if type(self) == type(other) \
                and self.name == other.name \
                and self.description == other.description \
                and self.len == other.len \
                and self.prompt_cards == other.prompt_cards \
                and self.response_cards == other.response_cards \
                and self.lang == other.lang:
            return True
        else:
            return False

    def add_card(self, card):
        """
        Add a Card to the Deck
        :param card: a Card object
        :return:
        """
        if isinstance(card, Card):
            self.cards.append(card)
        else:
            raise ValueError(f"Not a valid Card object. {type(card)} was passed")

    def remove_card(self, card):
        """
        Remove a Card from the Deck
        :param card: a Card object
        :return:
        """
        if isinstance(card, Card):
            self.cards.remove(card)
        else:
            raise ValueError(f"Not a valid Card object. {type(card)} was passed")
