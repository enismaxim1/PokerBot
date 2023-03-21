import os
import pygame
from poker_game import PokerGame, Action, Era
from player import Player
import math
from button import Button
import colors
from pygame_textinput import TextInputVisualizer, TextInputManager
from dimmer import *


class PokerUI:
    def __init__(self, poker_game, screen_size=(800, 650)):
        self.poker_game = poker_game
        self.screen_size = screen_size
        self.card_images = {}
        self.init_ui()
        self.load_card_images()
        self.load_table_image()

    def init_ui(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.game_surface= pygame.Surface(self.screen_size, pygame.SRCALPHA)
        pygame.display.set_caption("Poker")

    def update_buttons(self):
        # Create buttons for each action
        button_width, button_height = 100, 40
        button_x = self.screen_size[0] / 2
        button_y = self.screen_size[1] - button_height - 20
        valid_actions = self.poker_game.compute_valid_actions()
        num_buttons = len(valid_actions)

        self.buttons = [
            Button(self.game_surface, button_x - ((num_buttons - 1) / 2 - i) * (button_width + 10), button_y, button_width, button_height, action.value.capitalize(), action = action)
            for i, action in enumerate(valid_actions)
        ]

        self.text_input = None


    def draw_text(self, text, position, font_size=24, color=(255, 255, 255)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center = position)
        self.game_surface.blit(text_surface, text_rect)

    def load_card_images(self):
        suits = ['spades', 'clubs', 'hearts', 'diamonds']
        ranks = [str(i) for i in range(2, 11)] + ['jack', 'queen', 'king', 'ace']

        for suit in suits:
            for rank in ranks:
                image_name = f"{rank}_of_{suit}.png"
                image_path = os.path.join("res/card_images", image_name)
                self.card_images[f"{rank}_of_{suit}"] = pygame.image.load(image_path).convert_alpha()

    def load_table_image(self):
        image_path = os.path.join("res", "table_image.png")
        self.table_image = pygame.image.load(image_path).convert_alpha()

    def draw_cards(self, cards, position):
        card_width = 45
        margin = 10
        x, y = position

        for i, card in enumerate(cards):
            card_key = "_".join(str(card).split(" "))
            card_image = self.card_images[card_key]

            # Maintain aspect ratio while scaling
            original_width, original_height = card_image.get_size()
            aspect_ratio = float(original_height) / float(original_width)
            card_height = int(card_width * aspect_ratio)

            scaled_card_image = pygame.transform.smoothscale(card_image, (card_width, card_height))
            self.game_surface.blit(scaled_card_image, scaled_card_image.get_rect(center = (x + (i - (len(cards) - 1)/ 2) * (card_width + margin), y)))


    def draw_game(self):
        self.input_active = False
        self.update_game_state()
        self.game_surface.fill((34, 32, 33))


        original_width, original_height = self.table_image.get_size()
        aspect_ratio = float(original_height) / float(original_width)
        table_width = self.screen_size[0]
        table_height = int(table_width * aspect_ratio)

        scaled_table_image = pygame.transform.smoothscale(self.table_image, (table_width, table_height))
        self.game_surface.blit(scaled_table_image, scaled_table_image.get_rect(center = (self.screen_size[0] // 2, self.screen_size[1] // 2)))

        center_x, center_y = self.screen_size[0] // 2, self.screen_size[1] // 3
        radius = min(self.screen_size) // 3
        num_players = len(self.poker_game.players)
        angle_step = 2 * math.pi / num_players

        for i, player in enumerate(self.poker_game.players):
            angle = i * angle_step
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))

            if player == self.poker_game.current_player:
                color = colors.YELLOW1  # Highlight the active player with a yellow color
            elif player not in self.poker_game.active_players:
                color = colors.DARKGRAY
            else:
                color = colors.WHITE

            self.draw_text(f"{player.name}", (x, y), color=color)
            self.draw_text(f"Stack: {player.stack}", (x, y + 20), color=color)
            self.draw_text(f"Wager: {player.current_wager}", (x, y + 40), color=color)
            self.draw_cards(player.hand, (x, y + 90))

        self.draw_cards(self.poker_game.community_cards, (center_x, center_y + 100))
        
        self.draw_text(f"{self.poker_game.pot}", (center_x, center_y + 25))
        # self.darken_background()


    def update_game_state(self):
        self.update_buttons()

    def update_draw(self):
        for button in self.buttons:
            button.draw()
        self.screen.blit(self.game_surface, (0,0))
        if self.text_input:
            input, pos = self.text_input
            x,y = pos
            _, size = input.font_object.size('100')
            self.screen.blit(input.surface, (x, y - size / 2))



    def dim_screen(self):
        dark_rect = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        dark_rect.fill((0, 0, 0, 128))
        self.game_surface.blit(dark_rect, (0,0))
    

    def create_text_input(self, position):
        font = pygame.font.SysFont(None, 25)
        manager = TextInputManager(validator = lambda input: not input or input.isdigit() and int(input) < 999999)
        input = TextInputVisualizer(manager=manager, font_object=font, font_color = colors.WHITE, cursor_color = colors.WHITE, cursor_blink_interval = 700)
        self.text_input = (input, position)
        return input

    def create_input_prompt(self, position):
        self.input_active = True
        self.dim_screen()
        x, y = position
        text = 'Amount: '
        self.draw_text(text, position)
        self.create_text_input((x + 40, y))


    def run(self):
        clock = pygame.time.Clock()
        running = True
        self.draw_game()

        while running:
            events = pygame.event.get()
            # Feed it with events every frame
            if self.text_input:
                input, _ = self.text_input
                input.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.text_input:
                        input, _ = self.text_input
                        amount = int(input.value)
                        self.poker_game.perform_action(Action.RAISE, amount = amount)
                        self.text_input = None
                        self.draw_game()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.text_input:
                        self.text_input = None
                        self.draw_game()

                # Handle button events
                for button in self.buttons:
                    if button.is_clicked(event):

                        if button.action == Action.BET or button.action == Action.RAISE:
                            if not self.input_active:
                                self.create_input_prompt((button.x + button.width + 20, button.y) )
                        else:
                            self.poker_game.perform_action(button.action)
                            self.draw_game()

                        break


            self.update_draw()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    # Initialize your PokerGame instance here, e.g., poker_game = PokerGame(...)
    players = [Player("Kan", 2000), Player("Maxim", 2000), Player("Andrew", 2000)]
    poker_game = PokerGame(players)
    poker_ui = PokerUI(poker_game)
    poker_ui.run()