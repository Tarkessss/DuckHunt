import pygame
import random

width, height = 1500, 1000


class Duck(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/duck.png'), (300, 200))

    def __init__(self, *group):
        super().__init__(*group)
        self.side = random.choice([True, False])
        self.duck_y = random.randint(30, 400)
        self.image = Duck.image
        self.rect = self.image.get_rect()
        if self.side:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x = width + 300
            self.rect.y = self.duck_y
        else:
            self.rect.x = -600
            self.rect.y = self.duck_y

    def update(self):
        if self.side:
            self.rect.x -= 10
        else:
            self.rect.x += 10
        if ((not self.side and self.rect.x > width) or
                (self.side and self.rect.x < -600)):
            self.despawn_duck()

    def despawn_duck(self):
        self.kill()
