import os
import sys

import pygame

pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cursor(pygame.sprite.Sprite):
    image = load_image('target.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]


all_sprites = pygame.sprite.Group()
cur = Cursor(all_sprites)
running = True
fps = 60
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            all_sprites.update(event)
            pygame.mouse.set_visible(False)

    screen.fill('lightblue')
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
