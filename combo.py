import pygame
import sys
import random
from dataclasses import dataclass
import sched, time

# Импортируем классы Duck, Cursor, Ground
from duck import Duck
from cursor import Cursor
from ground import Ground

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1280, 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SaddleBrown = (139, 69, 19)
Chocolate = (210, 105, 30)
LightCyan = (224, 255, 255)

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Многооконное приложение")

# Фон первого окна
background = pygame.image.load("data/fon2.jpg")
background2 = pygame.image.load("data/fon66.gif")

# Кнопки
start_button = pygame.Rect(500, 300, 300, 100)
mode1_button = pygame.Rect(500, 130, 340, 110)
mode2_button = pygame.Rect(500, 260, 340, 110)
mode3_button = pygame.Rect(500, 390, 340, 110)
finish_button = pygame.Rect(800, 500, 300, 100)
mode9_button = pygame.Rect(500, 390, 340, 110)
back_button = pygame.Rect(900, 400, 240, 80)  # Новая кнопка для возвращения ко второму окну
back_to_first_button = pygame.Rect(1000, 500, 240, 80)  # Новая кнопка для перехода к первому окну


def draw_button(surface, rect, color, text_color, text):
    """Функция для отрисовки кнопки"""
    pygame.draw.rect(surface, SaddleBrown, rect, width=4)  # Рамка кнопки
    pygame.draw.rect(surface, Chocolate, rect.inflate(-8, -8))  # Внутренняя часть кнопки

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
        draw_button(screen, start_button, GREEN, BLACK, "СТАРТ")  # Отображаем кнопку СТАРТ

        pygame.display.flip()


def second_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode1_button.collidepoint(event.pos):
                    third_window()
                elif mode2_button.collidepoint(event.pos):
                    print("Нажата кнопка Режим 2")
                elif mode3_button.collidepoint(event.pos):
                    print("Нажата кнопка Режим 3")
                if back_to_first_button.collidepoint(event.pos):
                    first_window()  # Переход

        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text = font.render("Выберите режим", True, (0, 0, 0))
        screen.blit(background2, (0, 0))

        draw_button(screen, mode1_button, RED, LightCyan, "Режим 1")
        draw_button(screen, mode2_button, BLUE, LightCyan, "Режим 2")
        draw_button(screen, mode3_button, GREEN, LightCyan, "Режим 3")
        draw_button(screen, back_to_first_button, RED, WHITE, "Назад")  # Отображаем кнопку "Назад к первому окну"

        pygame.display.flip()


def third_window():
    # Переменные для игры "Утки"
    size = WIDTH, HEIGHT
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

    score = 0
    font = pygame.font.Font('data/8-BIT WONDER.TTF', 74)
    win_font = pygame.font.Font('data/8-BIT WONDER.TTF', 128)

    def spawn_duck():
        nonlocal speed
        speed += 0.25
        Duck(speed, ducks)

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

        screen.fill('lightblue')
        ground_group.draw(screen)
        ducks.draw(screen)
        cursor_group.draw(screen)

        score_text = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 230, 20))
        if score == 1000:
            score_text = win_font.render("You win", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH - 1150, 300))

        if time_counter % 60 == 0:
            spawn_duck()
        ducks.update()
        pygame.display.flip()
        clock.tick(fps)
        time_counter += 1

    pygame.quit()
    sys.exit()


# Запуск первой функции
first_window()