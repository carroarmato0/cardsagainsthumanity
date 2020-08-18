import json
import uuid

from cah.card import Card
from cah.utils import convert_to_dict


class Player:
    """ A class representing a player """

    def __init__(self, websocket, username='', isAdmin=False):
        self.websocket = websocket
        self.username = username
        self.uuid = str(uuid.uuid4())
        self.cards = []
        self.points = 0
        self.isCzar = False
        self.isAdmin = isAdmin
        print("Player created: " + self.to_json())

    def __del__(self):
        self.websocket.close()
        print("Player destroyed: " + self.to_json())

    def add_card(self, card: Card):
        self.cards.append(card)
        print(self.username + " received: " + card.to_json())

    def remove_card(self, card: Card):
        self.cards.remove(card)
        print(self.username + " lost: " + card.to_json())

    def to_json_obj(self):
        """
        Return the JSON Object of this class
        :return: JSON Object
        """
        return {
            'uuid': self.uuid,
            'username': self.username,
            'points': self.points,
            'isCzar': self.isCzar,
            'isAdmin': self.isAdmin,
            'cards': [card.to_json_obj() for card in self.cards]}

    def to_json(self):
        """
        Return the JSON String of this class
        :return: JSON str
        """
        return json.dumps(self.to_json_obj(), default=convert_to_dict)
