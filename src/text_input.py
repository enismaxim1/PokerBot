import pygame
from pygame_textinput import TextInputVisualizer, TextInputManager
import colors

class TextInput():

    def __init__(self, screen, position, font_size, on_submit, on_exit, on_submit_keys = [], on_exit_keys = []):
        font = pygame.font.Font("res/Mulish/static/Mulish-ExtraBold.ttf", font_size)
        manager = TextInputManager(validator = lambda input: not input or input.isdigit() and int(input) < 999999)
        self.input = TextInputVisualizer(manager=manager, font_object=font, font_color = colors.WHITE, cursor_color = colors.WHITE, cursor_blink_interval = 700)
        self.screen = screen
        self.position = position
        self.on_submit = on_submit
        self.on_exit = on_exit
        self.on_submit_keys = on_submit_keys
        self.on_exit_keys = on_exit_keys



    def draw_text(self, text, position, font_size=16, color=(255, 255, 255)):
        font = pygame.font.Font("res/Mulish/static/Mulish-Bold.ttf", font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center = position)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        text = 'Amount: '
        x, y = self.position
        self.draw_text(text, (x + 20, y))
        self.screen.blit(self.input.surface, (x + 55, y - 10))

    def update(self, events):
        self.input.update(events)
        self.draw()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.on_submit_keys:
                self.on_submit(self.input.value)
            if event.key in self.on_exit_keys:
                self.on_exit()