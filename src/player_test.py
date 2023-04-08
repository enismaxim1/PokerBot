import unittest
from player import *

class PlayerTest(unittest.TestCase):


    def test_to_dict(self):
        player = Player("max", 2000, "id")
        self.assertEqual(player.to_dict(), {'name': 'max', 'stack': 2000, 'client_id': 'id', 'previous_wager': 0, 'current_wager': 0})
    
    def test_from_dict(self):
        player_dict = {
            'name': 'max',
            'stack': 2000,
            'client_id': 'id',
            'previous_wager': 0,
            'current_wager': 0
        }
        self.assertEqual(Player('max', 2000, 'id'), Player.from_dict(player_dict))

    def test_reversible(self):
        player = Player('max', 2000, 'id')
        self.assertEqual(player, Player.from_dict(player.to_dict()))


if __name__ == "__main__":
    unittest.main()