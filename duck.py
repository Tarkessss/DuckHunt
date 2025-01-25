import pygame
import random

width, height = 1500, 1000


class Duck(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/duck.png'), (300, 200))
    image_dead = pygame.transform.scale(pygame.image.load('data/dead_duck.png'), (230, 130))

    def __init__(self,speed, *group):
        super().__init__(*group)
        self.side = random.choice([True, False])
        self.duck_y = random.randint(30, 400)
        self.speed = speed
        self.image = Duck.image
        self.rect = self.image.get_rect()
        if self.side:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x = width + 300
            self.rect.y = self.duck_y
        else:
            self.rect.x = -600
            self.rect.y = self.duck_y
        self.falling = False
        self.fall_speed = 0

    def update(self):
        if self.falling:
            self.fall_speed += 1
            self.rect.y += self.fall_speed
            if self.rect.y > height:
                self.kill()
        else:
            if self.side:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if ((not self.side and self.rect.x > width) or
                    (self.side and self.rect.x < -600)):
                self.despawn_duck()

    def despawn_duck(self):
        self.image = Duck.image_dead
        self.falling = True
        self.fall_speed = 0

