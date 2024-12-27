import duck
import cursor
import pygame

pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)


cursor_group = pygame.sprite.Group()
ducks = pygame.sprite.Group()
cur = cursor.Cursor(cursor_group)
duck_spr = duck.Duck(ducks)
running = True
fps = 60
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            cursor_group.update(event)
            pygame.mouse.set_visible(False)

    screen.fill('lightblue')
    ducks.draw(screen)
    cursor_group.draw(screen)
    ducks.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
