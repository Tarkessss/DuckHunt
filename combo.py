import pygame
import sys
import sqlite3
import random
# import pyautogui
import os
import sys
from duck import Duck
from duck2 import Duck2
from cursor import Cursor
from ground import Ground

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            mode INTEGER,
            score INTEGER
        )''')
    conn.commit()
    conn.close()


def save_score(score, mode):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (mode, score) VALUES (?, ?)', (mode, score))
    conn.commit()
    conn.close()


def get_top_scores(mode, limit=3):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT score FROM scores WHERE mode = ? ORDER BY score DESC LIMIT ?', (mode, limit))
    scores = c.fetchall()
    conn.close()
    return [s[0] for s in scores]


pygame.init()
size = WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode(size)
cursor_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
ducks = pygame.sprite.Group()
cur = Cursor(cursor_group)
ground_spr = Ground(ground_group)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SaddleBrown = (139, 69, 19)
Chocolate = (210, 105, 30)
LightCyan = (224, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Многооконное приложение")
background = pygame.image.load("data/ground.png")
start_button = pygame.Rect(500, 300, 300, 100)
mode1_button = pygame.Rect(500, 130, 340, 110)
mode2_button = pygame.Rect(500, 260, 340, 110)
mode3_button = pygame.Rect(500, 390, 340, 110)
finish_button = pygame.Rect(800, 500, 300, 100)
back_to_first_button = pygame.Rect(1000, 500, 240, 80)
exit_to_lobby_button = pygame.Rect(1200, 900, 250, 90)


def draw_button(surface, rect, color, text_color, text):
    pygame.draw.rect(surface, SaddleBrown, rect, width=4)
    pygame.draw.rect(surface, Chocolate, rect.inflate(-8, -8))
    font = pygame.font.Font(None, 64)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
    surface.blit(text_surface, text_rect)


def first_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    second_window()
        screen.blit(background, (0, 0))
        draw_button(screen, start_button, GREEN, BLACK, "СТАРТ")
        pygame.display.flip()


def second_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode1_button.collidepoint(event.pos):
                    third_window(mode=1)
                elif mode2_button.collidepoint(event.pos):
                    third_window(mode=2)
                elif mode3_button.collidepoint(event.pos):
                    print("Нажата кнопка Режим 3")
                if back_to_first_button.collidepoint(event.pos):
                    first_window()
        screen.fill(WHITE)
        draw_button(screen, mode1_button, RED, LightCyan, "Режим 1")
        draw_button(screen, mode2_button, BLUE, LightCyan, "Режим 2")
        draw_button(screen, mode3_button, GREEN, LightCyan, "Режим 3")
        draw_button(screen, back_to_first_button, RED, WHITE, "Назад")
        mode1_scores = get_top_scores(mode=1)
        mode2_scores = get_top_scores(mode=2)
        mode3_scores = get_top_scores(mode=3)
        font = pygame.font.Font(None, 36)
        score_text1 = font.render("Режим 1 Рекорды: " + str(mode1_scores), True, (0, 0, 0))
        score_text2 = font.render("Режим 2 Рекорды: " + str(mode2_scores), True, (0, 0, 0))
        score_text3 = font.render("Режим 3 Рекорды: " + str(mode3_scores), True, (0, 0, 0))
        screen.blit(score_text1, (WIDTH - 400, 20))
        screen.blit(score_text2, (WIDTH - 400, 60))
        screen.blit(score_text3, (WIDTH - 400, 100))
        pygame.display.flip()


def third_window(mode):
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
    game_over_font = pygame.font.Font('data/8-BIT WONDER.TTF', 74)
    reload_sound = pygame.mixer.Sound('data/reloading.wav')
    shot_sound = pygame.mixer.Sound('data/shot.wav')
    duck_sound = pygame.mixer.Sound('data/duck_sound.wav')
    background_music = pygame.mixer.Sound('data/background_music.wav')

    if mode == 1:
        def spawn_duck():
            # global speed
            # speed += 0.25
            Duck(speed, load_image("duck.png"), 3, 1, 200, 200, ducks)

        background_music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor_group.update(event)
                    pygame.mouse.set_visible(False)
                    mouse_x, mouse_y = event.pos
                    if exit_to_lobby_button.collidepoint(event.pos):
                        pygame.mouse.set_visible(True)
                if event.type == pygame.MOUSEBUTTONDOWN and cool_down == 0:
                    shot_sound.play()
                    reload_sound.play()
                    recoil_y = random.randint(30, 60)
                    recoil_x = random.randint(-30, 30)
                    # pyautogui.moveRel(recoil_x, -recoil_y)
                    cur.rect.y -= recoil_y
                    cur.rect.x += recoil_x
                    cool_down = 40
                    Cursor.cd(cur)
                    for d in ducks:
                        if d.rect.collidepoint(event.pos):
                            d.despawn_duck()
                            score += 1
                            duck_sound.play()
                            break
                        if exit_to_lobby_button.collidepoint(event.pos):
                            save_score(score, mode)
                            first_window()

            screen.fill('lightblue')
            ground_group.draw(screen)
            ducks.draw(screen)
            cursor_group.draw(screen)

            score_text = font.render(str(score), True, (0, 0, 0))
            screen.blit(score_text, (width - 230, 20))
            if score == 1000:
                score_text = win_font.render("You win", True, (0, 0, 0))
                screen.blit(score_text, (WIDTH - 1150, 300))
                save_score(score, mode)
                top_scores = get_top_scores(mode)
                print(f"Top Scores for mode {mode}: {top_scores}")
            draw_button(screen, exit_to_lobby_button, GREEN, BLACK, "Выход ")

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

    elif mode == 2:
        running = True
        game_over = False

        def spawn_duck():
            nonlocal speed
            speed += 0.25
            Duck2(speed, load_image("duck.png"), 3, 1, 200, 200, ducks)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    cursor_group.update(event)
                    mouse_x, mouse_y = event.pos
                    if exit_to_lobby_button.collidepoint(event.pos):
                        pygame.mouse.set_visible(True)
                    else:
                        pygame.mouse.set_visible(False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for d in ducks:
                        if d.rect.collidepoint(event.pos):
                            d.despawn_duck()
                            score += 1
                            break
                    if exit_to_lobby_button.collidepoint(event.pos):
                        save_score(score, mode)
                        first_window()

            if not game_over:
                screen.fill('lightblue')
                ground_group.draw(screen)
                ducks.draw(screen)
                cursor_group.draw(screen)
                score_text = font.render(str(score), True, (0, 0, 0))
                screen.blit(score_text, (WIDTH - 230, 20))
                if score == 1000:
                    score_text = win_font.render("You win", True, (0, 0, 0))
                    screen.blit(score_text, (WIDTH - 1150, 300))
                    save_score(score, mode)
                    top_scores = get_top_scores(mode)
                    print(f"Top Scores for mode {mode}: {top_scores}")
                draw_button(screen, exit_to_lobby_button, GREEN, BLACK, "Выход ")

                if time_counter % 60 == 0:
                    spawn_duck()

                ducks.update()
                for d in ducks:
                    if d.rect.x < -600 or d.rect.x > WIDTH + 300:
                        game_over = True
                        break
            else:
                game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
                screen.fill('lightblue')
                screen.blit(game_over_text, (WIDTH // 2 - 325, HEIGHT // 2 - 100))

            pygame.display.flip()
            clock.tick(fps)
            time_counter += 1

    pygame.quit()
    sys.exit()


init_db()
first_window()