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
        lines,append(pygame.Rect(i,door_pos + door_width,line_whidth,screen_height - door ))