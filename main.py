import duck
import cursor
import ground
import pygame
import sched, time

pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)

cursor_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
ducks = pygame.sprite.Group()
cur = cursor.Cursor(cursor_group)
ground_spr = ground.Ground(ground_group)

running = True
fps = 60
clock = pygame.time.Clock()
time_counter = 0


def spawn_duck():
    duck.Duck(ducks)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            cursor_group.update(event)
            pygame.mouse.set_visible(False)

    screen.fill('lightblue')
    ground_group.draw(screen)
    ducks.draw(screen)
    cursor_group.draw(screen)
    if time_counter % 60 == 0:
        spawn_duck()
    ducks.update()
    pygame.display.flip()
    clock.tick(fps)
    time_counter += 1

pygame.quit()
