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

if __name__ == "__main__":
    unittest.main()