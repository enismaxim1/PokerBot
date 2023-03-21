import card
import itertools as it
from enum import Enum
from functools import total_ordering

LOW_STRAIGHT_RANKS = [2, 3, 4, 5, 14]

class HandTypes(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

@total_ordering
class Hand():

    def __init__(self, cards):
        self.cards = cards
        self.type = self.compute_hand_type(cards)

    def compute_hand_type(self, cards):
        if is_straight_flush(cards):
            return HandTypes.STRAIGHT_FLUSH
        if is_four_of_a_kind(cards):
            return HandTypes.FOUR_OF_A_KIND
        if is_full_house(cards):
            return HandTypes.FULL_HOUSE
        if is_flush(cards):
            return HandTypes.FLUSH
        if is_straight(cards):
            return HandTypes.STRAIGHT
        if is_three_of_a_kind(cards):
            return HandTypes.THREE_OF_A_KIND
        if is_two_pair(cards):
            return HandTypes.TWO_PAIR
        if is_pair(cards):
            return HandTypes.PAIR
        return HandTypes.HIGH_CARD
    
    def __lt__(self, other):
        if isinstance(other, Hand):
            return compare_hands(self, other) < 0
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Hand):
            return compare_hands(self, other) == 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Hand):
            return compare_hands(self, other) > 0
        return NotImplemented



def is_straight_flush(cards):
    return is_straight(cards) and is_flush(cards)

def is_four_of_a_kind(cards):
    ranks = [card.rank for card in cards]
    for rank in set(ranks):
        if ranks.count(rank) == 4:
            return True
    return False

def is_full_house(cards):
    return is_pair(cards) and is_three_of_a_kind(cards)

def is_flush(cards):
    suits = [card.suit for card in cards]
    if len(set(suits)) == 1:
        return True
    return False

def is_straight(cards):
    ranks = [card.rank for card in cards]
    ranks.sort()
    # check if cards form a low straight
    if ranks == LOW_STRAIGHT_RANKS:
        return True
    for i in range(len(ranks) - 1):
        if ranks[i + 1] - ranks[i] != 1:
            return False
    return True

def is_three_of_a_kind(cards):
    ranks = [card.rank for card in cards]
    for rank in set(ranks):
        if ranks.count(rank) == 3:
            return True
    return False

def is_two_pair(cards):
    ranks = [card.rank for card in cards]
    num_pairs = 0
    for rank in set(ranks):
        if ranks.count(rank) == 2:
            num_pairs += 1
    if num_pairs == 2:
        return True
    return False

def is_pair(cards):
    ranks = [card.rank for card in cards]
    for rank in set(ranks):
        if ranks.count(rank) == 2:
            return True
    return False


# find the best 5 card hand out of the cards provided
def best_hand(cards):
    if len(cards) < 5:
        raise Exception(f"Not enough cards in hand {cards}")
    
    best = None
    for cards in it.combinations(cards, 5):
        hand = Hand(cards)
        if not best or hand > best:
            best = hand
    return best


# returns positive value if hand1 is better than hand2, 0 if they tie, and negative value if hand2 is better than hand1
def compare_hands(hand1, hand2):
    if hand1.type.value != hand2.type.value:
        return hand1.type.value - hand2.type.value
    # break ties by ranks
    ranks1 = [card.rank for card in hand1.cards]
    ranks2 = [card.rank for card in hand2.cards]
    ranks1.sort()
    ranks2.sort()
    # if we have a low straight, assign lower score than any other straight
    if ranks1 == LOW_STRAIGHT_RANKS:
        return 0 if ranks2 == LOW_STRAIGHT_RANKS else -1
    for i in reversed(range(len(ranks1))):
        if ranks1[i] > ranks2[i]:
            return 1
        if ranks2[i] > ranks1[i]:
            return -1
    return 0
