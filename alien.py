import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """a class representing a single alien in the fleet"""

    def __init__(self, ai_game):
        """initialize the alien in starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load the alien image and set its rect attribute
        self.image = pygame.image.load('course/invaders/images/butt1.jpg')
        self.rect = self.image.get_rect()

        #start each alien near ther top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the sliens exact position
        self.x = float(self.rect.x)

    def update(self):
        """move aliens to the right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True