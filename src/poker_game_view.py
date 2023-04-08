from player import Player
from poker_game import *

class PokerGameView:

    def __init__(self, game_dict):
        self.initialize(game_dict)

    def initialize(self, game_dict):
        self.current_era = Era(game_dict['current_era'])
        self.community_cards = [Card.from_dict(card_dict) for card_dict in game_dict['community_cards']]
        self.visible_cards = [Card.from_dict(card_dict) for card_dict in game_dict['visible_cards']]
        self.players = [Player.from_dict(player_dict) for player_dict in game_dict['players']]
        self.active_players = [Player.from_dict(player_dict) for player_dict in game_dict['active_players']]
        self.unfolded_players = [Player.from_dict(player_dict) for player_dict in game_dict['unfolded_players']]
        self.valid_actions = [Action(action) for action in game_dict['valid_actions']]
        self.current_player = Player.from_dict(game_dict['current_player']) if game_dict['current_player'] else None
        self.action_finished = game_dict['action_finished']
        self.pot = game_dict['pot']
        self.dealer_pos = game_dict['dealer_pos']
        self.payout_map = game_dict['payout_map']

    def __repr__(self):
        return (
            f"current era: {self.current_era}\n"
            f"community cards: {self.community_cards}\n"
            f"visible cards: {self.visible_cards}\n"
            f"players: {self.players}\n"
            f"active players: {self.active_players}\n"
            f"unfolded players: {self.unfolded_players}\n"
            f"valid actions: {self.valid_actions}\n"
            f"current player: {self.current_player}\n"
            f"action_finished: {self.action_finished}\n"
            f"pot: {self.pot}\n"
            f"dealer position: {self.dealer_pos}\n"
            f"payout_map: {self.payout_map}"
        )
