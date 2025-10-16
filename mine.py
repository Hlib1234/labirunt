import pygame
import random
import os
import time

# Ініціалізація pygame
pygame.init()

# Параметри екрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Піксельний лабіринт")

# Кольори
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметри лабіринту
cell_size = 40
cols = screen_width // cell_size
rows = screen_height // cell_size

# Завантаження спрайта гравця
sprite_path = "image.png"
if os.path.exists(sprite_path):
    player_img = pygame.image.load(sprite_path).convert_alpha()
    player_img = pygame.transform.scale(player_img, (40, 40))
else:
    player_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(player_img, (255, 0, 0), (20, 20), 20)

# Завантаження зображення фінішу
finish_path = "072ee6c8-abfd-4285-9d67-67025e212aa2.png"
if os.path.exists(finish_path):
    finish_img = pygame.image.load(finish_path).convert_alpha()
    finish_img = pygame.transform.scale(finish_img, (80, 50))
else:
    finish_img = pygame.Surface((80, 50))
    finish_img.fill((255, 215, 0))
    pygame.draw.rect(finish_img, (255, 0, 0), (0, 0, 80, 50), 5)

# Клас гравця
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 4

    def move(self, keys, walls):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Рух по осі X
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right

        # Рух по осі Y
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

        # Обмеження екрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def draw(self, surface):
        surface.blit(player_img, (self.rect.x, self.rect.y))


# Генерація випадкового лабіринту (DFS)
def generate_maze():
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []
    start = (random.randrange(0, rows, 2), random.randrange(0, cols, 2))
    maze[start[0]][start[1]] = 0
    stack.append(start)

    while stack:
        r, c = stack[-1]
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        carved = False

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr // 2][c + dc // 2] = 0
                stack.append((nr, nc))
                carved = True
                break

        if not carved:
            stack.pop()
    return maze


# Перетворення лабіринту на список стін
def maze_to_walls(maze):
    walls = []
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                walls.append(pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size))
    return walls


# Фініш на краях карти
def get_edge_finish_cell(maze):
    edge_cells = []
    for c in range(cols):
        if maze[0][c] == 0:
            edge_cells.append((0, c))
        if maze[rows - 1][c] == 0:
            edge_cells.append((rows - 1, c))
    for r in range(rows):
        if maze[r][0] == 0:
            edge_cells.append((r, 0))
        if maze[r][cols - 1] == 0:
            edge_cells.append((r, cols - 1))
    if not edge_cells:
        return (0, 0)
    return random.choice(edge_cells)


# Створення лабіринту
maze = generate_maze()
walls = maze_to_walls(maze)

# Вільні клітинки
free_cells = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0]

# Випадковий спавн і фініш
spawn_r, spawn_c = random.choice(free_cells)
finish_r, finish_c = get_edge_finish_cell(maze)

# Якщо співпали — міняємо фініш
while (spawn_r, spawn_c) == (finish_r, finish_c):
    finish_r, finish_c = get_edge_finish_cell(maze)

# Координати
spawn_x = spawn_c * cell_size
spawn_y = spawn_r * cell_size
finish_rect = pygame.Rect(finish_c * cell_size + 5, finish_r * cell_size + 5, 30, 30)

# Гравець
player = Player(spawn_x, spawn_y)
clock = pygame.time.Clock()

# Таймер
total_time = 180  # 3 хвилини = 180 секунд
start_ticks = pygame.time.get_ticks()  # час початку гри

running = True
game_over = False
lost = False

# Основний цикл
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    if not game_over and not lost:
        keys = pygame.key.get_pressed()
        player.move(keys, walls)

        # Перевірка фінішу
        if player.rect.colliderect(finish_rect):
            game_over = True

        # Перевірка часу
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # у секундах
        time_left = max(0, int(total_time - seconds))
        if time_left <= 0:
            lost = True

        # Малювання
        screen.fill(BLACK)
        for wall in walls:
            pygame.draw.rect(screen, GREEN, wall)

        # Фініш
        screen.blit(finish_img, (finish_rect.x - 20, finish_rect.y - 10))
        player.draw(screen)

        # Таймер у правому верхньому кутку
        font = pygame.font.Font(None, 40)
        minutes = time_left // 60
        seconds = time_left % 60
        timer_text = font.render(f"{minutes:02}:{seconds:02}", True, WHITE)
        screen.blit(timer_text, (screen_width - 120, 20))

    elif game_over:
        # Перемога
        screen.fill(BLACK)
        font = pygame.font.Font(None, 80)
        text = font.render("🎉 ТИ ПЕРЕМІГ! 🎉", True, (255, 215, 0))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))

    elif lost:
        # Програш
        screen.fill(BLACK)
        font = pygame.font.Font(None, 80)
        text = font.render("⌛ ТИ ПРОГРАВ!", True, RED)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
