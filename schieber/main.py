from dataclasses import dataclass, field
from enum import Enum
from random import shuffle, choice
from typing import List
import numpy as np

class CardSuit(Enum):
    DIAMOND = 1
    HEARTS = 2
    SPADES = 3
    CLUBS = 4

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

@dataclass
class Card:
    suit: CardSuit
    card_type: CardType

    def __str__(self):
        return '-'.join([self.card_type.name, self.suit.name])

    def __repr__(self):
        return self.__str__()

    def is_trumpf(self, trumpf_suit: CardSuit = None):
        """
        Checks whether the card has the same suit as the
        given :trumpf_suit. False if no suit is provided.
        """
        if trumpf_suit is None:
            return False

        return trumpf_suit == self.suit

    def strength(self, trumpf_suit: CardSuit = None):
        """
        Determines the value of the card, given a trumpf suit
        (as some values depend on the choice of trumpf). 
        """
        is_trumpf = self.is_trumpf(trumpf_suit)

        strength = {
            CardType.SIX: 9 if is_trumpf else 19,
            CardType.SEVEN: 8 if is_trumpf else 18,
            CardType.EIGHT: 7 if is_trumpf else 17,
            CardType.NINE: 2 if is_trumpf else 16,
            CardType.TEN: 6 if is_trumpf else 15,
            CardType.JACK: 1 if is_trumpf else 14,
            CardType.QUEEN: 5 if is_trumpf else 13,
            CardType.KING: 4 if is_trumpf else 12,
            CardType.ACE: 3 if is_trumpf else 11,
        }

        return strength[self.card_type]

    def value(self, trumpf_suit: CardSuit = None):
        """
        Determines the value of the card, given a trumpf suit
        (as some values depend on the choice of trumpf). 
        """
        is_trumpf = self.is_trumpf(trumpf_suit)

        card_values = {
            CardType.SIX: 0,
            CardType.SEVEN: 0,
            CardType.EIGHT: 0,
            CardType.NINE: 14 if is_trumpf else 0,
            CardType.TEN: 10,
            CardType.JACK: 20 if is_trumpf else 2,
            CardType.QUEEN: 3,
            CardType.KING: 4,
            CardType.ACE: 11,
        }

        return card_values[self.card_type]

class Deck:
    cards: List[Card] = []

    def __init__(self):
        for s in CardSuit._member_map_.values():
            for t in CardType._member_map_.values():
                self.cards.append(Card(s, t))

    def num_cards(self):
        return len(self.cards)

    def shuffle_deck(self):
        shuffle(self.cards)


@dataclass
class Team:
    label: str

@dataclass
class Player:
    label: str
    team: Team
    hand_cards: List[Card] = field(default_factory=list)

    def deal_cards(self, hand_cards: List[Card]):
        self.hand_cards = hand_cards

    def choose_trumpf(self):
        # TODO
        return choice(list(CardSuit))

    def choose_card(self):
        # TODO
        card = choice(self.hand_cards)
        self.hand_cards.remove(card)
        return card


@dataclass
class Turn:
    player: Player
    card: Card

    def __str__(self):
        return f"[{self.player.team.label}{self.player.label}] {self.card}"

    def __repr__(self):
        self.__str__()

@dataclass
class Round:
    player_order: List[int]
    winning_player: Player = None
    turns: List[Turn] = field(default_factory=list)

    def add_turn(self, turn):
        self.turns.append(turn)

    def determine_winner(self, trumpf_suit: CardSuit):
        turn_cards = list(map(lambda t: t.card, self.turns))
        strengths = list(map(lambda c: c.strength(trumpf_suit), turn_cards))

        win_card_idx = np.argmin(strengths)
        self.winning_player = self.turns[win_card_idx].player
        return self.winning_player

@dataclass
class SchieberGame:
    players: List[Player]
    deck: Deck = Deck()
    rounds: List[Round] = field(default_factory=list)
    
    trumpf_suit: CardSuit = None
    initial_player: Player = None
    player_order = List[int]

    def deal_cards(self):
        dealt_cards = np.array_split(self.deck.cards, self.num_players())

        for pid, player in enumerate(self.players):
            player.deal_cards(list(dealt_cards[pid]))

    def num_players(self):
        return len(self.players)

    def play_game(self):
        self.trumpf_suit = None
        self.player_order = list(range(len(self.players)))
        self.deck.shuffle_deck()
        self.deal_cards()
        self.initial_player = self.players[0]
        self.trumpf_suit = self.initial_player.choose_trumpf()
        print(f"\n{self.trumpf_suit.name} is Trumpf\n")

        num_rounds = self.deck.num_cards() // self.num_players()
        for i in range(num_rounds):
            self.rounds.append(self.play_round())

    def play_round(self):
        start_player_idx = self.players.index(self.initial_player)
        self.player_order = np.mod(np.arange(self.num_players()) + start_player_idx, 4)

        r = Round(self.player_order)

        for pid in self.player_order:
            player = self.players[pid]
            card = player.choose_card()
            r.add_turn(Turn(player, card))

        self.initial_player = r.determine_winner(self.trumpf_suit)
        
        print('-' * 30)
        for t in r.turns:
            print(t, '\t', '*' if t.player == r.winning_player else '', '\t', '+' if t.card.suit == self.trumpf_suit else '')
        print('')

        return r


def main():
    team_a = Team('A')
    team_b = Team('B')
    teams = [team_a, team_b]

    player_a1 = Player('1', team_a)
    player_b2 = Player('2', team_b)
    player_a3 = Player('3', team_a)
    player_b4 = Player('4', team_b)
    players = [player_a1, player_b2, player_a3, player_b4]

    game = SchieberGame(players)
    game.play_game()

    # import code; code.interact(local=dict(globals(), **locals()))


if __name__ == '__main__':
    main()
