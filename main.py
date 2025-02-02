import pygame
import random
import pyautogui


class Duck(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/duck.png'),
                                   (300, 200))
    image_dead = pygame.transform.scale(pygame.image.load('data/dead_duck.png'),
                                        (230, 130))

    def __init__(self, speed, *group):
        super().__init__(*group)
        self.side = random.choice([True, False])
        self.duck_y = random.randint(30, 400)
        self.speed = speed
        self.image = Duck.image
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
        else:
            self.time_counter -= 1
            if self.time_counter == 0:
                self.kill()

    def despawn_duck(self):
        duck_sound.play()
        if not self.side:
            self.image = Duck.image_dead
        else:
            self.image = pygame.transform.flip(Duck.image_dead, True, False)
        self.falling = True
        self.fall_speed = 0


class Ground(pygame.sprite.Sprite):
    image = pygame.image.load('data/ground.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Ground.image, (1500, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800


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


pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)
cursor_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
ducks = pygame.sprite.Group()
cur = Cursor(cursor_group)
ground_spr = Ground(ground_group)

running = True
fps = 60
clock = pygame.time.Clock()
time_counter = 0
speed = 5
cool_down = 0
score = 0
font = pygame.font.Font('data/8-BIT WONDER.TTF', 74)
win_font = pygame.font.Font('data/8-BIT WONDER.TTF', 128)
reload_sound = pygame.mixer.Sound('data/reloading.wav')
shot_sound = pygame.mixer.Sound('data/shot.wav')
duck_sound = pygame.mixer.Sound('data/duck_sound.wav')


def spawn_duck():
    global speed
    speed += 0.25
    Duck(speed, ducks)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            cursor_group.update(event)
            pygame.mouse.set_visible(False)
        if event.type == pygame.MOUSEBUTTONDOWN and cool_down == 0:
            shot_sound.play()
            reload_sound.play()
            recoil_y = random.randint(30, 60)
            recoil_x = random.randint(-30, 30)
            pyautogui.moveRel(recoil_x, -recoil_y)
            cur.rect.y -= recoil_y
            cur.rect.x += recoil_x
            cool_down = 40
            Cursor.cd(cur)
            for d in ducks:
                if d.rect.collidepoint(event.pos):
                    d.despawn_duck()
                    score += 1
                    break

    screen.fill('lightblue')
    ground_group.draw(screen)
    ducks.draw(screen)
    cursor_group.draw(screen)

    score_text = font.render(str(score), True, (0, 0, 0))
    screen.blit(score_text, (width - 230, 20))
    if score == 100:
        score_text = win_font.render("You win", True, (0, 0, 0))
        screen.blit(score_text, (width - 1150, 300))

    if time_counter % 60 == 0:
        spawn_duck()
    ducks.update()
    pygame.display.flip()
    clock.tick(fps)
    time_counter += 1
    if cool_down > 0:
        cool_down -= 1
    else:
        Cursor.ready(cur)

pygame.quit()
