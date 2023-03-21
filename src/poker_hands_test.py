import unittest
from card import *
from poker_hands import *

class PokerHandsTest(unittest.TestCase):

    def test_straight_flush(self):
        card_1 = Card(11, Suit.CLUB)
        card_2 = Card(12, Suit.CLUB)
        card_3 = Card(13, Suit.CLUB)
        card_4 = Card(14, Suit.CLUB)
        card_5 = Card(10, Suit.CLUB)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.STRAIGHT_FLUSH)

    def test_four_of_a_kind(self):
        card_1 = Card(11, Suit.CLUB)
        card_2 = Card(11, Suit.SPADE)
        card_3 = Card(11, Suit.HEART)
        card_4 = Card(11, Suit.DIAMOND)
        card_5 = Card(10, Suit.CLUB)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.FOUR_OF_A_KIND)

    def test_full_house(self):
        card_1 = Card(3, Suit.CLUB)
        card_2 = Card(3, Suit.DIAMOND)
        card_3 = Card(3, Suit.SPADE)
        card_4 = Card(2, Suit.CLUB)
        card_5 = Card(2, Suit.HEART)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.FULL_HOUSE)

    def test_flush(self):
        card_1 = Card(3, Suit.SPADE)
        card_2 = Card(2, Suit.SPADE)
        card_3 = Card(5, Suit.SPADE)
        card_4 = Card(10, Suit.SPADE)
        card_5 = Card(4, Suit.SPADE)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.FLUSH)

    def test_straight(self):
        card_1 = Card(3, Suit.CLUB)
        card_2 = Card(4, Suit.DIAMOND)
        card_3 = Card(14, Suit.SPADE)
        card_4 = Card(5, Suit.CLUB)
        card_5 = Card(2, Suit.HEART)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.STRAIGHT)

    def test_three_of_a_kind(self):
        card_1 = Card(3, Suit.CLUB)
        card_2 = Card(3, Suit.DIAMOND)
        card_3 = Card(3, Suit.SPADE)
        card_4 = Card(2, Suit.CLUB)
        card_5 = Card(14, Suit.HEART)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.THREE_OF_A_KIND)


    def test_two_pair(self):
        card_1 = Card(3, Suit.CLUB)
        card_2 = Card(3, Suit.DIAMOND)
        card_3 = Card(5, Suit.SPADE)
        card_4 = Card(2, Suit.CLUB)
        card_5 = Card(2, Suit.HEART)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.TWO_PAIR)

    def test_pair(self):
        card_1 = Card(3, Suit.CLUB)
        card_2 = Card(10, Suit.DIAMOND)
        card_3 = Card(5, Suit.SPADE)
        card_4 = Card(2, Suit.CLUB)
        card_5 = Card(2, Suit.HEART)
        hand = Hand([card_1, card_2, card_3, card_4, card_5])
        self.assertEqual(hand.type, HandTypes.PAIR)

    def test_best_hand_1(self):
        card_1 = Card(11, Suit.CLUB)
        card_2 = Card(12, Suit.CLUB)
        card_3 = Card(13, Suit.CLUB)
        card_4 = Card(14, Suit.DIAMOND)
        card_5 = Card(10, Suit.CLUB)
        card_6 = Card(14, Suit.CLUB)
        card_7 = Card(14, Suit.SPADE)
        hand = best_hand([card_1, card_2, card_3, card_4, card_5, card_6, card_7])
        self.assertEqual(set(hand.cards), set([card_1, card_2, card_3, card_5, card_6]))
        self.assertEqual(hand.type, HandTypes.STRAIGHT_FLUSH)

    def test_best_hand_2(self):
        card_1 = Card(11, Suit.CLUB)
        card_2 = Card(13, Suit.CLUB)
        card_3 = Card(12, Suit.CLUB)
        card_4 = Card(10, Suit.DIAMOND)
        card_5 = Card(12, Suit.SPADE)
        card_6 = Card(12, Suit.DIAMOND)
        card_7 = Card(14, Suit.SPADE)
        hand = best_hand([card_1, card_2, card_3, card_4, card_5, card_6, card_7])
        self.assertEqual(hand.type, HandTypes.STRAIGHT)

    def test_compare_hands_1(self):
        hand1_cards = []
        hand1_cards.append(Card(3, Suit.CLUB))
        hand1_cards.append(Card(10, Suit.DIAMOND))
        hand1_cards.append(Card(5, Suit.SPADE))
        hand1_cards.append(Card(2, Suit.CLUB))
        hand1_cards.append(Card(13, Suit.HEART))
        hand1 = Hand(hand1_cards)
        hand2_cards = []
        hand2_cards.append(Card(3, Suit.DIAMOND))
        hand2_cards.append(Card(10, Suit.SPADE))
        hand2_cards.append(Card(6, Suit.CLUB))
        hand2_cards.append(Card(2, Suit.DIAMOND))
        hand2_cards.append(Card(13, Suit.DIAMOND))
        hand2 = Hand(hand2_cards)
        self.assertLess(hand1, hand2)

    def test_compare_hands_2(self):
        hand1_cards = []
        hand1_cards.append(Card(3, Suit.DIAMOND))
        hand1_cards.append(Card(10, Suit.DIAMOND))
        hand1_cards.append(Card(5, Suit.DIAMOND))
        hand1_cards.append(Card(2, Suit.DIAMOND))
        hand1_cards.append(Card(13, Suit.DIAMOND))
        hand1 = Hand(hand1_cards)
        hand2_cards = []
        hand2_cards.append(Card(3, Suit.SPADE))
        hand2_cards.append(Card(10, Suit.SPADE))
        hand2_cards.append(Card(5, Suit.SPADE))
        hand2_cards.append(Card(2, Suit.SPADE))
        hand2_cards.append(Card(13, Suit.SPADE))
        hand2 = Hand(hand2_cards)
        self.assertEqual(hand1, hand2)

    def test_compare_hands_3(self):
        hand1_cards = []
        hand1_cards.append(Card(2, Suit.DIAMOND))
        hand1_cards.append(Card(14, Suit.CLUB))
        hand1_cards.append(Card(3, Suit.DIAMOND))
        hand1_cards.append(Card(4, Suit.DIAMOND))
        hand1_cards.append(Card(5, Suit.DIAMOND))
        hand1 = Hand(hand1_cards)
        hand2_cards = []
        hand2_cards.append(Card(6, Suit.SPADE))
        hand2_cards.append(Card(3, Suit.CLUB))
        hand2_cards.append(Card(4, Suit.SPADE))
        hand2_cards.append(Card(2, Suit.SPADE))
        hand2_cards.append(Card(5, Suit.SPADE))
        hand2 = Hand(hand2_cards)
        self.assertLess(hand1, hand2)
        



if __name__ == "__main__":
    unittest.main()