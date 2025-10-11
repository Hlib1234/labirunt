import pygame
import random

pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Лфбіринт")

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

line_whidth = 10
line_offset = 20
line_gap = 40
door_width = 20
door_gap = 40
max_openings_per_line = 5

player_radius = 10
player_speed = 5
player_x = screen_width - 12
player_y = screen_height - line_offset
lines = []
for i in range(0, screen_width, line_gap):
    rect = pygame.Rect(i,0,line_whidth, screen_height)
    num_openings = random.randint(1,max_openings_per_line)
    if num_openings == 1:
        door_pos = random.randint(line_offset + door_width, screen_height - line_offset - door_width)
        lines.append(pygame.Rect(i,0,line_whidth,door_pos - door_width))
        lines.append(pygame.Rect(i,door_pos + door_width,line_whidth,screen_height - door_pos - door_width))

    else:
        opening_positions = [0] + sorted([random.randint(line_offset + door_width, screen_height - line_offset - door_width)for _ in range(num_openings)]) + [screen_height]
        for j in range(num_openings):
            lines.append(pygame.Rect(i, opening_positions[j], line_whidth, opening_positions[j + 1]- opening_positions[j] - door_width))
clock = pygame.time.Clock
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT():
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_radius:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen_width - player_radius:
        player_x += player_speed
    elif keys[pygame.K_UP] and  player_y > player_radius:
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and player_y < screen_height - player_radius:
        player_y += player_speed

    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    for line in lines :
        if line.colliderect(player_rect):
            if player_x > line.left and player_x < line.right:
                if player_y < line.too:
                    player_y = line.top - player_radius
                else:
                    player_y = line.bottom + player_radius
            elif player_y > line.top and player_y < line.bottom:
                if player_x < line.left:
                    player_x = line.left - player_radius
                else:
                    player_x = line.right + player_radius
    screen.fill(black)
    for line in lines:
        pygame.draw.rect(screen, green, line)
    pygame.draw.circle(screen, red, (player_x, player_y), player_radius)
    player.display.update()
    clock.tick(60)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    