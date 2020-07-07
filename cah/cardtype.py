from enum import Enum


class CardType(str, Enum):
    PROMPT = "prompt",
    RESPONSE = "response",
