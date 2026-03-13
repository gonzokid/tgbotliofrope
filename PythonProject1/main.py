import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Избегай блоки!")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Игрок
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# Блоки (враги)
blocks = []
block_size = 40
block_speed = 5
block_spawn_rate = 30  # Чем меньше, тем чаще появляются блоки

# Счет и уровень
score = 0
level = 1
font = pygame.font.Font(None, 36)

# Время
clock = pygame.time.Clock()
FPS = 60

# Игровой цикл
running = True
game_over = False


def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))


def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, RED, (block[0], block[1], block_size, block_size))


def draw_ui():
    score_text = font.render(f"Счет: {score}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    # Подсказки управления
    controls_text = font.render("Управление: ← → стрелки", True, GREEN)
    screen.blit(controls_text, (WIDTH - 300, 10))


def check_collision():
    for block in blocks:
        if (player_x < block[0] + block_size and
                player_x + player_size > block[0] and
                player_y < block[1] + block_size and
                player_y + player_size > block[1]):
            return True
    return False


def show_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, RED)
    final_score_text = font.render(f"Ваш счет: {score}", True, WHITE)
    restart_text = font.render("Нажми R для перезапуска", True, GREEN)
    quit_text = font.render("Нажми Q для выхода", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
    screen.blit(final_score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
    screen.blit(quit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 60))

    pygame.display.flip()


def reset_game():
    global player_x, player_y, blocks, score, level, game_over, block_speed
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 20
    blocks = []
    score = 0
    level = 1
    block_speed = 5
    game_over = False


# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Создание новых блоков
        if random.randint(1, block_spawn_rate) == 1:
            block_x = random.randint(0, WIDTH - block_size)
            blocks.append([block_x, -block_size])

        # Движение блоков
        for block in blocks[:]:
            block[1] += block_speed

            # Удаление блоков за пределами экрана и увеличение счета
            if block[1] > HEIGHT:
                blocks.remove(block)
                score += 1

                # Повышение уровня каждые 10 очков
                if score % 10 == 0:
                    level += 1
                    block_speed += 1  # Увеличиваем сложность

        # Проверка столкновений
        if check_collision():
            game_over = True

        # Отрисовка
        screen.fill(BLACK)
        draw_player()
        draw_blocks()
        draw_ui()

    else:
        show_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()