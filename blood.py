import pygame
import sys
import os
import random
all_sprites = pygame.sprite.Group()
FPS = 25
size = width, height = 1000, 1000
GRAVITY = 1.25
screen_rect = (0, 0, width, height)


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("data/blood(1).png")]
    fire.append(pygame.transform.scale(fire[0], (1, 2)))
    # for scale in (5, 5, 5):
    #     fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # print(position)
    # количество создаваемых частиц
    particle_count = 1
    # возможные скорости
    numbers = range(1, 2)
    s = []
    for _ in range(particle_count):
        x = Particle(position, random.choice(numbers), random.choice(numbers))
        s.append(x)
    return s


all_sprites = pygame.sprite.Group()


def __main__():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos())

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()


if __name__ == '__main__':
    __main__()