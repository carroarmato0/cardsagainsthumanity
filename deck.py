class Deck:
    """ A Class representing a deck of cards """

    def __init__(self, id, name, description, cards):
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
        cards = []
        for card in self._cards:
            if card.type == "black":
                cards.append(card)
        return cards

    def white_cards(self):
        cards = []
        for card in self._cards:
            if card.type == "white":
                cards.append(card)
        return cards

    def __len__(self):
        return self._cards.len()

