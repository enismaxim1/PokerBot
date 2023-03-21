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

class Era(Enum):
    BEGINNING = 'beginning'
    PREFLOP = 'preflop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

class PokerGame:
    def __init__(self, players, small_blind = 5, big_blind = 10):
        self.players = players
        self.active_players = players.copy()
        self.deck = Deck()
        self.community_cards = []
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.dealer_pos = 0
        self.dealer = players[self.dealer_pos]
        self.pot = 0
        self.current_era = Era.BEGINNING
        self.next_era()

    def next_era(self):
        self.clear_wagers()
        era = self.current_era
        if era == Era.BEGINNING:
            self.preflop()
        elif era == Era.PREFLOP:
            self.flop()
        elif era == Era.FLOP:
            self.turn()
        elif era == Era.TURN:
            self.river()
        elif era == Era.RIVER:
            self.showdown()

    def deal_hole_cards(self):
        for player in self.players:
            player.hand = self.deck.deal(2)

    def deal_community_cards(self, num_cards):
        self.community_cards.extend(self.deck.deal(num_cards))

    def preflop(self):
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

    def flop(self):
        self.fix_postflop_positions()
        self.current_era = Era.FLOP
        self.deal_community_cards(3)

    def turn(self):
        self.fix_postflop_positions()
        self.current_era = Era.TURN
        self.deal_community_cards(1)

    def river(self):
        self.fix_postflop_positions()
        self.current_era = Era.RIVER
        self.deal_community_cards(1)
    
    def showdown(self):
        self.current_era = Era.SHOWDOWN
        print("FUCKFUCK")

        # Determine the best hand for each player
        player_hands = {}
        for player in self.active_players:
            full_hand = player.hand + self.community_cards
            player_hands[player] = poker_hands.best_hand(full_hand)

        # Find the winner(s) of the showdown
        winners = []
        best_hand_found = None
        print(player_hands)
        for player, hand in player_hands.items():
            if not best_hand_found or hand > best_hand_found:
                winners = [player]
                best_hand_found = hand
            elif hand == best_hand_found:
                winners.append(player)

        # Distribute the pot among the winners
        print(winners)
        split_pot = self.pot // len(winners)
        for winner in winners:
            winner.stack += split_pot
            print(winner.stack)
            print(f"{winner.name} wins {split_pot} with a {best_hand_found.type}: {best_hand_found.cards}")
            

    def next_hand(self):
        self.active_players = self.players.copy()
        self.deck = Deck()
        self.community_cards = []
        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)
        self.dealer = self.players[self.dealer_pos]
        self.pot = 0
        self.current_era = Era.BEGINNING
        self.next_era()

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

    def clear_wager(self, player):
        self.pot += player.current_wager
        player.current_wager = 0

    def clear_wagers(self):
        for player in self.active_players:
           self.clear_wager(player)
        self.current_bet = 0


    def perform_action(self, action, amount = 0):
        self.print_game_state()
        next_player = self.next_player(self.current_player)

        if action == Action.FOLD:
            # fix dealer position, if necessary
            if self.current_player == self.dealer:
                self.dealer = self.previous_player(self.current_player)
            self.active_players.remove(self.current_player)
            self.clear_wager(self.current_player)

        elif action == Action.BET or action == Action.RAISE:
            self.raise_bet(self.current_player, amount)

        elif action == Action.CHECK:
            pass

        elif action == Action.CALL:
            call_amount = self.current_bet - self.current_player.current_wager
            self.current_player.wager(call_amount)

        if len(self.active_players) == 1:
            self.clear_wagers()
            self.active_players[0].stack += self.pot
            self.next_hand()
        if self.last_player == self.current_player:
            self.next_era()
        else:
            self.current_player = next_player

    
    def raise_bet(self, player, amount):
        # TODO: consider cases where raise amount is smaller than bet (like in an all-in)
        if amount < self.current_bet:
            raise Exception("Cannot raise to smaller than existing pot size")
        self.current_bet = amount
        player.wager(amount - player.current_wager)
        self.last_player = self.previous_player(self.current_player)

    def compute_valid_actions(self):
        # TODO: let players all-in even when they can't raise
        actions = [Action.FOLD]
        call_amount = self.current_bet - self.current_player.current_wager
        min_raise = 2 * self.current_bet

        if call_amount == 0:
            actions.append(Action.CHECK)
        if self.current_bet == 0:
            actions.append(Action.BET)
        if call_amount > 0 and self.current_player.stack >= call_amount:
            actions.append(Action.CALL)
        if self.current_bet > 0 and min_raise - self.current_player.current_wager < self.current_player.stack:
            actions.append(Action.RAISE)

        return actions

   