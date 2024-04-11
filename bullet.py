import pygame
from pygame.sprite import Group, Sprite

class Bullet(Sprite):
    """A Class that manges bullets fired from the ship"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a rectangle at (0,0) then move it to the correct position
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midbottom = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Moves the bullets across the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)