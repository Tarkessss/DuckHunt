import pygame
import random

width, height = 1500, 1000


class Duck(pygame.sprite.Sprite):
    image_dead = pygame.transform.scale(pygame.image.load('data/dead_duck.png'),
                                        (230, 130))

    def __init__(self, speed, sheet, columns, rows, x, y, *group):
        self.side = random.choice([True, False])
        self.anim_time_count = 0
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.duck_y = random.randint(30, 400)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.death = False
        self.time_counter = 120
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
        if self.anim_time_count % 20 == 0 and not self.falling and not self.death:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.falling:
            self.fall_speed += 1
            self.rect.y += self.fall_speed
            if self.side:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if self.rect.y > height - 300:
                self.falling = False
                self.death = True
        elif not self.falling and not self.death:
            if self.side:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if ((not self.side and self.rect.x > width) or
                    (self.side and self.rect.x < -600)):
                self.despawn_duck()
        elif self.rect.y > height:
            self.kill()

        else:
            self.time_counter -= 1
            if self.time_counter == 0:
                self.kill()
        self.anim_time_count += 1

    def despawn_duck(self):
        if not self.side:
            self.image = Duck.image_dead
        else:
            self.image = pygame.transform.flip(Duck.image_dead, True, False)
        self.falling = True
        self.fall_speed = 0

    def cut_sheet(self, sheet, columns, rows):
        if self.side:
            sheet = self.image = pygame.transform.flip(sheet, True, False)
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
