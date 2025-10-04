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