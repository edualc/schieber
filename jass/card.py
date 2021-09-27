from dataclasses import dataclass
from enum import Enum
from typing import List

class CardType(Enum):
    SIX = 1
    SEVEN = 2
    EIGHT = 3
    NINE = 4
    TEN = 5
    JACK = 6
    QUEEN = 7
    KING = 8
    ACE = 9

class Suit(Enum):
    A = 1
    B = 2
    C = 3
    D = 4

"""
    https://en.wikipedia.org/wiki/Jass#Schieber_rules
"""

@dataclass
class Card:
    suit: Suit
    card_type: CardType

class Deck:
    cards: List[Card] = []

    def __init__(self):
        for s in Suit._member_map_.values():
            for t in CardType._member_map_.values():
                self.cards.append(Card(s, t))


import code; code.interact(local=dict(globals(), **locals()))