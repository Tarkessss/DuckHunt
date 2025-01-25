import pygame


class Ground(pygame.sprite.Sprite):
    image = pygame.image.load('data/ground.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Ground.image, (1500, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800
