import pygame


class Cursor(pygame.sprite.Sprite):
    ready_image = pygame.transform.scale(
        pygame.image.load('data/cur_ready.png'), (80, 80))
    cd_image = pygame.transform.scale(pygame.image.load('data/cur_cd.png'),
                                      (80, 80))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.ready_image
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 450
        self.ready = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]
            if not self.ready:
                self.image = Cursor.ready_image
            else:
                self.image = Cursor.cd_image

    def ready(self):
        self.ready = False

    def cd(self):
        self.ready = True
