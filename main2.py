import duck2
import cursor
import ground
import pygame

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
speed = 5
score = 0
font = pygame.font.Font('data/8-BIT WONDER.TTF', 74)
win_font = pygame.font.Font('data/8-BIT WONDER.TTF', 128)
game_over_font = pygame.font.Font('data/8-BIT WONDER.TTF', 74)
reload_sound = pygame.mixer.Sound('data/reloading.wav')
shot_sound = pygame.mixer.Sound('data/shot.wav')
duck_sound = pygame.mixer.Sound('data/duck_sound.wav')
background_music = pygame.mixer.Sound('data/background_music.wav')

def spawn_duck():
    global speed
    speed += 0.25
    duck2.Duck(speed, ducks)

game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            cursor_group.update(event)
            pygame.mouse.set_visible(False)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for d in ducks:
                if d.rect.collidepoint(event.pos):
                    d.despawn_duck()
                    score += 1
                    break

    if not game_over:
        screen.fill('lightblue')
        ground_group.draw(screen)
        ducks.draw(screen)
        cursor_group.draw(screen)

        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (width - 230, 20))

        if score == 1000:
            score_text = win_font.render("You win", True, (0, 0, 0))
            screen.blit(score_text, (width - 1150, 300))

        if time_counter % 60 == 0:
            spawn_duck()

        ducks.update()

        for d in ducks:
            if d.rect.x < -600 or d.rect.x > width + 300:
                game_over = True
                break

        pygame.display.flip()
    else:
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.fill('lightblue')
        screen.blit(game_over_text, (width // 2 - 325, height // 2 - 100))
        pygame.display.flip()

    clock.tick(fps)
    time_counter += 1

pygame.quit()