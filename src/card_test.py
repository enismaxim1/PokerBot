import unittest
from card import *

class CardTest(unittest.TestCase):

    def test_str(self):
        card_1 = Card(11, Suit.CLUB)
        card_2 = Card(12, Suit.CLUB)
        card_3 = Card(13, Suit.CLUB)
        card_4 = Card(14, Suit.CLUB)
        self.assertEqual(str(card_1), "jack of clubs")
        self.assertEqual(str(card_2), "queen of clubs")
        self.assertEqual(str(card_3), "king of clubs")
        self.assertEqual(str(card_4), "ace of clubs")

    def test_to_dict(self):
        card = Card(11, Suit.CLUB)
        self.assertEqual(card.to_dict(), {'rank': 11, 'suit': Suit.CLUB.value})
    
    def test_from_dict(self):
        card_dict = {'rank': 7, 'suit': Suit.HEART.value}
        self.assertEqual(Card.from_dict(card_dict), Card(7, Suit.HEART))

    def test_reversible(self):
        card = Card(11, Suit.CLUB)
        self.assertEqual(card, Card.from_dict(card.to_dict()))


if __name__ == "__main__":
    unittest.main()