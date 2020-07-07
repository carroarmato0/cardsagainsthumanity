class Card:
    """ A Class representing a Card """

    def __init__(self, type, content, pick=None, draw=None):
        """
        Initializer for Card
        :param type: "black" or "white" card
        :param content: The text on the card
        :param pick: How many white cards is required for this card. Only possible when type="black"
        :param draw: How many white cards should be refilled after using a card. Only possible when type="black"
        """
        if not type:
            raise ValueError(f"The card needs to have a type")
        if type != "black" and type != "white":
            raise ValueError(f"The card type needs to be either black or white. {type} was passed")
        if not content:
            raise ValueError(f"The card needs to have content")

        self.type = type
        self.content = content

        if pick is None:
            if type == "black":
                self.pick = 1
            elif type == "white":
                self.pick = 0
        else:
            if type == "black" and int(pick) < 1:
                raise ValueError(f"A black card always needs to have at least 1 answer card")
            if type == "white" and pick > 0:
                raise ValueError(f"A white card cannot have answer cards")
            self.pick = int(pick)

        if draw is None:
            if type == "black":
                self.draw = 1
            elif type == "white":
                self.draw = 0
        else:
            if type == "black" and draw <= 0:
                raise ValueError(f"A black card cannot have a draw value lower than 1. {draw} was passed")
            if type == "white" and draw != 0:
                raise ValueError(f"A white card cannot have a draw value. {draw} was passed")
            self.draw = int(draw)

    def type(self):
        """
        Returns the type of the card
        :return: The type of this card, either "black" or "white"
        """
        return self.type

    def content(self):
        """
        Returns the text on the card
        :return: the text on the card
        """
        return self.content

    def pick(self):
        """
        Returns the amount of white cards required.
        For a white cards this is 0.
        For a black card, this is >= 1.
        :return: the amount of cards necessary to play
        """
        return self.pick

    def draw(self):
        """
        Returns the amount of white cards that can be taken from a pile.
        For a white cards this is 0.
        For a black card, this is >= 1.
        Ideally this should not be too high (max 2), depending on the game mode.
        :return: the amount of white cards that should be taken
        """
        return self.draw

    def __eq__(self, other):
        """
        Validate object for equality
        :param other: the other object to compare to
        :return: True of False is the object is equal to this instance
        """
        if type(self) == type(other) \
                and self.type == other.type \
                and self.content == other.content \
                and self.pick == other.pick \
                and self.draw == other.draw:
            return True
        else:
            return False
