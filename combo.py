import pygame
import sqlite3
import random
import pyautogui
import os
import sys
from duck import Duck
from duck2 import Duck2
from cursor import Cursor
from ground import Ground


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def get_top_scores(mode, limit=1):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute(
        'SELECT score FROM scores WHERE mode = ? ORDER BY score DESC LIMIT ?',
        (mode, limit))
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
pygame.display.set_caption("DUCK HUNT GAME")
background = pygame.image.load("data/fon1.png")
background1 = pygame.image.load("data/fon22.png")
background3 = pygame.image.load("data/fon3.png")
start_button = pygame.Rect(350, 700, 800, 100)
mode1_button = pygame.Rect(100, 650, 340, 110)
mode2_button = pygame.Rect(500, 650, 500, 110)
mode3_button = pygame.Rect(1070, 650, 340, 110)
finish_button = pygame.Rect(900, 500, 300, 100)
back_to_first_button = pygame.Rect(625, 910, 240, 80)
exit_to_lobby_button = pygame.Rect(1200, 900, 250, 90)
Startfont = pygame.font.Font("data/8bitwonderrusbylyajka_nominal.otf", 17)

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
        draw_button(screen, start_button, RED, BLACK, "СТАРТ")
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
                    third_window(mode=3)
                if back_to_first_button.collidepoint(event.pos):
                    first_window()
        screen.blit(background1, (0, 0))
        draw_button(screen, mode1_button, RED, LightCyan, "Песочница")
        draw_button(screen, mode2_button, BLUE, LightCyan, "Не пропусти ни одной")
        draw_button(screen, mode3_button, GREEN, LightCyan, "На время")
        draw_button(screen, back_to_first_button, RED, WHITE, "Назад")
        mode1_scores = get_top_scores(mode=1)
        mode2_scores = get_top_scores(mode=2)
        mode3_scores = get_top_scores(mode=3)
        font = pygame.font.Font("data/8bitwonderrusbylyajka_nominal.otf", 17)
        Startfont = pygame.font.Font("data/8bitwonderrusbylyajka_nominal.otf", 17)
        score_text1 = font.render("Песочница рекорд " + str(*mode1_scores), True,
                                  (255, 255, 255))
        score_text2 = font.render("Не пропусти ни одной " + str(*mode2_scores), True,
                                  (255, 255, 255))
        score_text3 = font.render("На время рекорд " + str(*mode3_scores), True,
                                  (255, 255, 255))
        screen.blit(score_text1, (WIDTH - 400, 30))
        screen.blit(score_text2, (WIDTH - 400, 90))
        screen.blit(score_text3, (WIDTH - 400, 150))
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
    game_over_font2 = pygame.font.Font('data/8-BIT WONDER.TTF', 55)
    reload_sound = pygame.mixer.Sound('data/reloading.wav')
    shot_sound = pygame.mixer.Sound('data/shot.wav')
    duck_sound = pygame.mixer.Sound('data/duck_sound.wav')
    background_music = pygame.mixer.Sound('data/background_music.wav')

    if mode == 1:
        def spawn_duck():
            nonlocal speed
            speed += 0.25
            Duck(speed, load_image("duck.png"), 3, 1, 200, 200, ducks)

        background_music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor_group.update(event)
                    pygame.mouse.set_visible(False)
                    if exit_to_lobby_button.collidepoint(event.pos):
                        pygame.mouse.set_visible(True)
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
                            duck_sound.play()
                            break
                        if exit_to_lobby_button.collidepoint(event.pos):
                            background_music.stop()
                            save_score(score, mode)
                            first_window()

            screen.blit(background3, (0, 0))
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

        background_music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor_group.update(event)
                    pygame.mouse.set_visible(False)
                    if exit_to_lobby_button.collidepoint(event.pos):
                        pygame.mouse.set_visible(True)
                if event.type == pygame.MOUSEBUTTONDOWN and cool_down == 0:
                    shot_sound.play()
                    reload_sound.play()
                    recoil_y = random.randint(30, 60)
                    recoil_x = random.randint(-30, 30)
                    pyautogui.moveRel(recoil_x, -recoil_y)
                    cur.rect.y -= recoil_y
                    cur.rect.x += recoil_x
                    cool_down = 20
                    Cursor.cd(cur)
                    for d in ducks:
                        if d.rect.collidepoint(event.pos):
                            d.despawn_duck()
                            score += 1
                            duck_sound.play()
                            break
                        if exit_to_lobby_button.collidepoint(event.pos):
                            background_music.stop()
                            save_score(score, mode)
                            first_window()
            if time_counter % 60 == 0:
                spawn_duck()
            ducks.update()
            pygame.display.flip()
            clock.tick(fps)
            if cool_down > 0:
                cool_down -= 1
            else:
                Cursor.ready(cur)
            if not game_over:
                screen.blit(background3, (0, 0))
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
                draw_button(screen, exit_to_lobby_button, GREEN, BLACK,
                            "Выход ")

                ducks.update()
                for d in ducks:
                    if d.rect.x < -600 or d.rect.x > WIDTH + 300:
                        game_over = True
                        break
            else:
                game_over_text = game_over_font.render("Game over", True,
                                                       (255, 0, 0))
                screen.fill('lightblue')
                screen.blit(game_over_text,
                            (WIDTH // 2 - 325, HEIGHT // 2 - 100))
                draw_button(screen, exit_to_lobby_button, GREEN, BLACK,
                            "Выход ")

            pygame.display.flip()
            clock.tick(fps)
            time_counter += 1
    elif mode == 3:
        def spawn_duck():
            nonlocal speed
            speed += 0.25
            Duck(speed, load_image("duck.png"), 3, 1, 200, 200, ducks)

        time = 60
        background_music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                    cursor_group.update(event)
                    pygame.mouse.set_visible(False)
                    if exit_to_lobby_button.collidepoint(event.pos):
                        pygame.mouse.set_visible(True)
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
                            duck_sound.play()
                            break
                        if exit_to_lobby_button.collidepoint(event.pos):
                            background_music.stop()
                            save_score(score, mode)
                            first_window()

            screen.blit(background3, (0, 0))
            ground_group.draw(screen)
            ducks.draw(screen)
            cursor_group.draw(screen)
            draw_button(screen, exit_to_lobby_button, GREEN, BLACK, "Выход ")
            score_text = font.render(str(score), True, (0, 0, 0))
            screen.blit(score_text, (width - 230, 20))
            time_text = font.render(str(time), True, (0, 0, 0))
            screen.blit(time_text, (width - 830, 20))
            if time <= 15:
                time_text = font.render(str(time), True, (255, 0, 0))
                screen.blit(time_text, (width - 830, 20))
            if time <= 0:
                game_over_text = game_over_font2.render("Time is up your score "+str(score), True,
                                                       (255, 0, 0))
                screen.fill('lightblue')
                screen.blit(game_over_text,
                            (WIDTH // 2 - 500, HEIGHT // 2 - 100))
                save_score(score, mode)
                draw_button(screen, exit_to_lobby_button, GREEN, BLACK,
                            "Выход ")

            if time_counter % 60 == 0:
                spawn_duck()
                time -= 1
            ducks.update()
            pygame.display.flip()
            clock.tick(fps)
            time_counter += 1
            if cool_down > 0:
                cool_down -= 1
            else:
                Cursor.ready(cur)
    pygame.quit()
    sys.exit()


init_db()
first_window()
