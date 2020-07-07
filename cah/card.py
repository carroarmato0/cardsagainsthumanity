class Card:
    """ A Class representing a Card """

    def __init__(self, type, content, pick=0):
        """
        Initializer for Card
        :param type: "black" or "white" card
        :param content: The text on the card
        :param pick: How many white cards is required for this card. Only possible when type="black"
        """
        if not type:
            raise ValueError(f"The card needs to have a type")
        if type != "black" and type != "white":
            raise ValueError(f"The card type needs to be either black or white. {type} was passed")
        if not content:
            raise ValueError(f"The card needs to have content")
        if type == "black" and int(pick) < 1:
            raise ValueError(f"A black card always needs to have at least 1 answer card")
        if type == "white" and pick > 0:
            raise ValueError(f"A white card cannot have answer cards")
        self.type = type
        self.content = content
        self.pick = int(pick)

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

    def __eq__(self, other):
        """
        Validate object for equality
        :param other: the other object to compare to
        :return: True of False is the object is equal to this instance
        """
        if type(self) == type(other) \
                and self.type == other.type \
                and self.content == other.content \
                and self.pick == other.pick:
            return True
        else:
            return False
