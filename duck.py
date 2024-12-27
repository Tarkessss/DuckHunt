import pygame
import random


class Duck(pygame.sprite.Sprite):
    image = pygame.image.load('data/duck.png')

    def __init__(self, *group):
        super().__init__(*group)
        side = random.choice([True, False])
        self.image = Duck.image
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = 100

    def update(self):
        self.rect.x += 10
