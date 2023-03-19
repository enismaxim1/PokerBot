import random
from card import *

class Deck:

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(2, 15) for suit in Suit]

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]