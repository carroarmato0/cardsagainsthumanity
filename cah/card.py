import json

from cah.cardtype import CardType
from cah.utils import convert_to_dict


class Card:
    """ A Class representing a Card """

    def __init__(self, type: CardType, content: str, pick=None, draw=None):
        """
        Initializer for Card
        :param type: CardType.PROMPT or CardType.RESPONSE card
        :param content: The text on the card
        :param pick: How many response cards is required for this card. Only possible when type=CardType.PROMPT
        :param draw: How many response cards should be refilled after using a card. Only possible when type=CardType.PROMPT
        """
        if not type:
            raise ValueError(f"The card needs to have a type")
        if type != CardType.PROMPT and type != CardType.RESPONSE:
            raise ValueError(f"The card type needs to be either CardType.PROMPT or CardType.RESPONSE. {type} was passed")
        if not content:
            raise ValueError(f"The card needs to have content")

        self.type = type
        self.content = content

        if pick is None:
            if type == CardType.PROMPT:
                self.pick = 1
            elif type == CardType.RESPONSE:
                self.pick = 0
        else:
            if type == CardType.PROMPT and int(pick) < 1:
                raise ValueError(f"A Prompt card always needs to have at least 1 answer card")
            if type == CardType.RESPONSE and pick > 0:
                raise ValueError(f"A Response card cannot have answer cards")
            self.pick = int(pick)

        if draw is None:
            if type == CardType.PROMPT:
                self.draw = 1
            elif type == CardType.RESPONSE:
                self.draw = 0
        else:
            if type == CardType.PROMPT and draw <= 0:
                raise ValueError(f"A Prompt card cannot have a draw value lower than 1. {draw} was passed")
            if type == CardType.RESPONSE and draw != 0:
                raise ValueError(f"A Response card cannot have a draw value. {draw} was passed")
            self.draw = int(draw)

    def type(self):
        """
        Returns the type of the card
        :return: The type of this card, either CardType.PROMPT or CardType.RESPONSE
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
        Returns the amount of response cards required.
        For a response card this is 0.
        For a prompt card, this is >= 1.
        :return: the amount of cards necessary to play
        """
        return self.pick

    def draw(self):
        """
        Returns the amount of response cards that can be taken from a pile.
        For a response cards this is 0.
        For a prompt card, this is >= 1.
        Ideally this should not be too high (max 2), depending on the game mode.
        :return: the amount of response cards that should be taken
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

    def to_json_obj(self):
        """
        Return the JSON Object of this class
        :return: JSON Object
        """
        return {'type': self.type, 'content': self.content, 'pick': self.pick, 'draw': self.draw}

    def to_json(self):
        """
        Return the JSON String of this class
        :return: JSON str
        """
        return json.dumps(self.to_json_obj())
