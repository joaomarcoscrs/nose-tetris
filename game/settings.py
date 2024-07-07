# settings.py
import pygame

# Placeholder values that will be updated on initialization
SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE = 0, 0, 0

# This controls how many grid cells the screen is divided into
GRID_FACTOR = 25

# Function to get screen dimensions and grid size
def initialize_settings():
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    GRID_SIZE = SCREEN_WIDTH // GRID_FACTOR
    return SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE


GRID_LINE_WIDTH = 1
