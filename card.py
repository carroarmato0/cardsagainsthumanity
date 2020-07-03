class Card:
    """ A Class representing a Card """

    def __init__(self, type, content, answer_count=0):
        if not type:
            raise ValueError(f"The card needs to have a type")
        if type != "black" and type != "white":
            raise ValueError(f"The card type needs to be either black or white. {type} was passed")
        if not content:
            raise ValueError(f"The card needs to have content")
        if type == "black" and int(answer_count) < 1:
            raise ValueError(f"A black card always needs to have at least 1 answer card")
        if type == "white" and answer_count > 0:
            raise ValueError(f"A white card cannot have answer cards")
        self._type = type
        self._content = content
        self._answer_count = int(answer_count)

    def type(self):
        return self._type

    def content(self):
        return self._content

    def answer_count(self):
        return self._answer_count
