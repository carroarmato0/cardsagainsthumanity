from enum import Enum


class GamePhase(str, Enum):
    SETUP = "setup",
    CARDS_SELECTION = "draw",
    CARDS_REVELATION = "fold",
    END = "end"
