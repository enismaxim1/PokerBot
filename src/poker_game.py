from deck import Deck
from card import *
from enum import Enum
import poker_hands

class Action(Enum):
    FOLD = 'fold'
    CHECK = 'check'
    BET = 'bet'
    CALL = 'call'
    RAISE = 'raise'
    ALL_IN = 'all in'

class Era(Enum):
    BEGINNING = 'beginning'
    PREFLOP = 'preflop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    PAYOUT = 'payout'

class PokerGame:
    def __init__(self, players, small_blind = 5, big_blind = 10):
        self.initialize_game(players, small_blind, big_blind)
        self.dealer_pos = 0
        self.dealer = players[self.dealer_pos]
    
    def initialize_game(self, players, small_blind, big_blind):
        self.players = players
        self.active_players = players.copy()
        self.unfolded_players = players.copy()
        self.clear_wagers()
        self.action_finished = True
        self.deck = Deck()
        self.community_cards = []
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.current_era = Era.BEGINNING
        self.current_player = None

    def next_era(self):
        era = self.current_era
        self.update_wagers()

        if era == Era.PAYOUT:
            self.next_hand()
        # if everyone else folded, skip to payout era
        elif len(self.unfolded_players) == 1:
            payout_map = {self.unfolded_players[0]: self.pot}
            self.payout(payout_map)
        else:
            if era == Era.BEGINNING:
                self.preflop()
            elif era == Era.PREFLOP:
                self.flop()
            elif era == Era.FLOP:
                self.turn()
            elif era == Era.TURN:
                self.river()
            elif era == Era.RIVER:
                payout_map = self.showdown()
                self.payout(payout_map)

    def deal_hole_cards(self):
        for player in self.players:
            player.hand = self.deck.deal(2)

    def deal_community_cards(self, num_cards):
        self.community_cards.extend(self.deck.deal(num_cards))

    def preflop(self):
        if len(self.active_players) > 1:
            self.action_finished = False
        self.current_era = Era.PREFLOP
        self.deck.shuffle()
        sb = self.next_player(self.dealer)
        bb = self.next_player(sb)
        sb.wager(self.small_blind)
        bb.wager(self.big_blind)
        self.current_bet = self.big_blind
        self.current_player = self.next_player(bb)
        self.last_player = bb
        self.deal_hole_cards()
        self.print_game_state()

    def flop(self):
        if len(self.active_players) > 1:
            self.action_finished = False
            self.fix_postflop_positions()
        self.current_era = Era.FLOP
        self.deal_community_cards(3)

    def turn(self):
        if len(self.active_players) > 1:
            self.action_finished = False
            self.fix_postflop_positions()
        self.current_era = Era.TURN
        self.deal_community_cards(1)

    def river(self):
        if len(self.active_players) > 1:
            self.action_finished = False
            self.fix_postflop_positions()
        self.current_era = Era.RIVER
        self.deal_community_cards(1)
    
    def payout(self, payout_map):
        self.payout_map = payout_map
        for player, payout in payout_map.items():
            player.stack += payout
        self.pot = 0

        self.current_era = Era.PAYOUT
    
    def showdown(self):
        payout_map = {}

        # find all players invested in the pots
        all_player_wagers = {player: player.previous_wager for player in self.players}
        unfolded_player_wagers = {player: player.previous_wager for player in self.unfolded_players}

        # find amount these players have invested in their respective pots
        bets = set([player.previous_wager for player in self.unfolded_players]) 
        sorted_bets = list(sorted(bets))
        # Determine the best hand for each player
        player_hands = {}
        for player in self.unfolded_players:
            full_hand = player.hand + self.community_cards
            player_hands[player] = poker_hands.best_hand(full_hand)
        

        # loop through all pots
        for bet in sorted_bets:
            # determine pot size
            pot_size = 0
            for player in self.players:
                amount = min(bet, all_player_wagers[player])
                pot_size += amount
                all_player_wagers[player] -= amount
            # eligible winners are unfolded players who have bet this much
            eligible_players = [player for player in self.unfolded_players if unfolded_player_wagers[player] >= bet]

            # Find the winner(s) of the showdown
            winners = []
            best_hand_found = None
            for player in eligible_players:
                hand = player_hands[player]
                if not best_hand_found or hand > best_hand_found:
                    winners = [player]
                    best_hand_found = hand
                elif hand == best_hand_found:
                    winners.append(player)

            # Distribute the pot among the winners
            print("winners", winners)
            split_pot = pot_size // len(winners)
            for winner in winners:
                if winner not in payout_map:
                    payout_map[winner] = 0
                payout_map[winner] += split_pot
                print(winner.stack)
                print(f"{winner.name} wins {split_pot} with a {best_hand_found.type}: {best_hand_found.cards}")

        return payout_map



    def next_hand(self):
        self.initialize_game(self.players, self.small_blind, self.big_blind)
        for player in self.players:
            if player.stack == 0:
                player.stack = self.big_blind * 200
        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)
        self.dealer = self.players[self.dealer_pos]

    def next_player(self, player):
        player_index = self.active_players.index(player)
        return self.active_players[(player_index + 1) % len(self.active_players)]

    def previous_player(self, player):
        player_index = self.active_players.index(player)
        return self.active_players[(player_index - 1) % len(self.active_players)]
    
    def fix_postflop_positions(self):
        self.current_player = self.next_player(self.dealer)
        self.last_player = self.dealer
    
    # print the game state to the terminal
    def print_game_state(self):
        print("Current player", self.current_player)
        print("Dealer", self.dealer)
        print("Pot size:", self.pot)
        print("Community cards:", self.community_cards)
        for i, player in enumerate(self.players):
            print(f"Player {i}: {player.name}, Stack: {player.stack}, Hand: {player.hand}")
        print(f"Current bet: {self.current_bet}")

    # fix highest uncalled bet to align with highest called bet size
    def clip_highest_bet(self):
        wagers = [(player.current_wager, player) for player in self.unfolded_players]
        wagers.sort(key = lambda p: p[0], reverse = True)
        # if there is an uncalled bet
        if len(wagers) >= 2 and wagers[0][0] > wagers[1][0]:
            uncalled_bet, uncalled_player = wagers[0]
            called_bet, _ = wagers[1]
            diff = uncalled_bet - called_bet
            uncalled_player.stack += diff
            uncalled_player.current_wager -= diff
            if uncalled_player not in self.active_players:
                self.active_players.append(uncalled_player)
            
    def update_wagers(self):
        self.clip_highest_bet()
        for player in self.players:
           self.pot += player.current_wager
           player.update_wager()
        self.current_bet = 0
        

    def clear_wagers(self):
        for player in self.players:
            player.previous_wager = 0
            player.current_wager = 0

    # removes player from the action
    def remove_player(self, player):
        # fix dealer position, if necessary
        if player == self.dealer:
            self.dealer = self.previous_player(player)
        self.active_players.remove(player)

    def perform_action(self, action, amount = 0):
        if action not in self.compute_valid_actions():
            return False

        next_player = self.next_player(self.current_player)
        if action == Action.FOLD:
            self.remove_player(self.current_player)
            self.unfolded_players.remove(self.current_player)

        elif action == Action.BET or action == Action.RAISE:
            difference = amount - self.current_player.current_wager
            if difference > self.current_player.stack:
                return False
            if amount < 2 * self.current_bet and difference != self.current_player.stack:
                return False
            self.raise_bet(self.current_player, amount)

        elif action == Action.CHECK:
            pass

        elif action == Action.CALL:
            call_amount = self.current_bet - self.current_player.current_wager
            self.current_player.wager(call_amount)

        elif action == Action.ALL_IN:
            self.raise_bet(self.current_player, self.current_player.stack + self.current_player.current_wager)
            
        if self.current_player.stack == 0:
            self.remove_player(self.current_player)

        if self.last_player == self.current_player:
            self.current_player = None
            self.action_finished = True
        else:
            self.current_player = next_player

        return True

    
    def raise_bet(self, player, amount):
        bet_raised = True if amount > self.current_bet else False
        self.current_bet = max(self.current_bet, amount)
        player.wager(amount - player.current_wager)
        if bet_raised:
            self.last_player = self.previous_player(self.current_player)

    def compute_valid_actions(self):

        actions = [Action.FOLD]
        call_amount = self.current_bet - self.current_player.current_wager
        min_raise = 2 * self.current_bet

        if call_amount == 0:
            actions.append(Action.CHECK)
        if self.current_bet == 0:
            actions.append(Action.BET)
        if call_amount > 0 and self.current_player.stack > call_amount:
            actions.append(Action.CALL)
        if self.current_bet > 0 and min_raise - self.current_player.current_wager < self.current_player.stack:
            actions.append(Action.RAISE)
        if Action.BET not in actions and Action.RAISE not in actions:
            actions.append(Action.ALL_IN)

        return actions

   