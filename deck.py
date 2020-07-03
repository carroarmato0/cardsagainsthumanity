class Deck:
    """ A Class representing a deck of cards """

    def __init__(self, id, name, description, cards):
        """
        Initializer for the Deck
        :param id: a unique identified for this deck
        :param name: a short title/name for this deck
        :param description: the description for this deck
        :param cards: a list of cards, ideally a combination of black and white types
        """
        if not id:
            raise ValueError(f"Deck id cannot be empty")
        if not name:
            raise ValueError(f"Deck name cannot be empty")
        if not isinstance(cards, list):
            raise ValueError(f"Supplied cards is not a list")

        self._id = id
        self._name = name
        self._description = description
        self._cards = cards

    def black_cards(self):
        """
        Get all the black cards in the deck
        :return: list of black cards
        """
        cards = []
        for card in self._cards:
            if card.type == "black":
                cards.append(card)
        return cards

    def white_cards(self):
        """
        Get all the white cards in the deck
        :return: list of white cards
        """
        cards = []
        for card in self._cards:
            if card.type == "white":
                cards.append(card)
        return cards

    def id(self):
        """
        Return the ID of this deck
        :return: id of this deck
        """
        return self._id

    def name(self):
        """
        Return the Name of this deck
        :return: name of this deck
        """
        return self._name

    def description(self):
        """
        Return the Description of this deck
        :return: description of this deck
        """
        return self._description

    def __len__(self):
        """
        Get the amount of cards in the deck
        :return: the amount of cards in the deck
        """
        return self._cards.len()

