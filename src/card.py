from enum import Enum

class Suit(Enum):
    SPADE = "spades"
    CLUB = "clubs"
    HEART = "hearts"
    DIAMOND = "diamonds"


class Card:

    def __init__(self, rank: int,  suit: Suit):
        if int(rank) != rank:
            raise Exception(f"rank {rank} is not integer")
        if rank < 2 or rank > 14:
            raise Exception(f"rank {rank} is out of bounds")
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank == 11:
            rank_str = "jack"
        elif self.rank == 12:
            rank_str = "queen"
        elif self.rank == 13:
            rank_str = "king"
        elif self.rank == 14:
            rank_str = "ace"
        else:
            rank_str = str(self.rank)
        return f"{rank_str} of {self.suit.value}"