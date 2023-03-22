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
    