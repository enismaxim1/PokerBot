import pygame 
import colors

class Button:
    def __init__(self, screen, x, y, width, height, text, color=colors.GRAY40, hover_color = colors.GRAY60, font_size=18, active = True, action = None):
        self.screen = screen
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rect = pygame.Rect(x - width / 2, y - height / 2, width, height)
        self.text = text
        self.hover_color = hover_color
        self.color = color
        self.font_size = font_size
        self.active = active
        self.action = action

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        pygame.draw.rect(self.screen, current_color, self.rect, 0)  # Fill the button with the current_color
        font = pygame.font.Font("res/Mulish/static/Mulish-Bold.ttf", self.font_size)
        text_surface = font.render(self.text, True, colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    # def handle_event(self, event):
    #     if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_RETURN:
    #                     if self.text_input:
    #                         input, _ = self.text_input
    #                         amount = int(input.value)
    #                         if self.poker_game.perform_action(Action.RAISE, amount = amount):
    #                             self.text_input = None
    #                             self.draw_game()
    #                 if event.key == pygame.K_ESCAPE:
    #                     if self.text_input:
    #                         self.text_input = None
    #                         self.draw_game()
    #                 if event.key == pygame.K_f:
    #                     if self.poker_game.perform_action(Action.FOLD):
    #                         self.draw_game()
    #                 if event.key == pygame.K_k:
    #                     if self.poker_game.perform_action(Action.CHECK):
    #                         self.draw_game()
    #                 if event.key == pygame.K_c:
    #                     if self.poker_game.perform_action(Action.CALL):
    #                         self.draw_game()
    #                 if event.key == pygame.K_r:
    #                     valid_actions = poker_game.compute_valid_actions()
    #                     if Action.BET in valid_actions or Action.RAISE in valid_actions:
    #                         if not self.input_active:
    #                             # TODO: fix bug in line below
    #                             self.create_input_prompt((button.x + button.width, button.y) )
    