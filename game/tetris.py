import pygame
import random
from .settings import initialize_settings
from .colors import WHITE, SHAPE_COLORS, DARK_GRAY
from .shapes import SHAPES

class Tetris:
    def __init__(self):
        self.screen_width, self.screen_height, self.grid_size = initialize_settings()
        self.grid = [[0 for _ in range(10)] for _ in range(self.screen_height // self.grid_size)]
        self.current_shape = self.get_new_shape()
        self.current_color = random.choice(SHAPE_COLORS)
        self.shape_x = 3
        self.shape_y = 0
        self.game_over = False

    def get_new_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self, screen):
        for y in range(self.screen_height // self.grid_size):
            for x in range(10):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x], (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size))
                pygame.draw.rect(screen, DARK_GRAY, (x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size), 1)

    def draw_shape(self, screen):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, self.current_color, ((self.shape_x + x) * self.grid_size, (self.shape_y + y) * self.grid_size, self.grid_size, self.grid_size))

    def move_shape(self, dx, dy):
        self.shape_x += dx
        self.shape_y += dy

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def freeze_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.grid[self.shape_y + y][self.shape_x + x] = self.current_color
        self.current_shape = self.get_new_shape()
        self.current_color = random.choice(SHAPE_COLORS)
        self.shape_x = 3
        self.shape_y = 0

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        while len(new_grid) < self.screen_height // self.grid_size:
            new_grid.insert(0, [0 for _ in range(10)])
        self.grid = new_grid

    def is_valid_move(self, dx, dy):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= self.screen_height // self.grid_size or self.grid[new_y][new_x] != 0:
                        return False
        return True

    def update(self):
        if self.is_valid_move(0, 1):
            self.shape_y += 1
        else:
            self.freeze_shape()
            self.clear_lines()
            if not self.is_valid_move(0, 0):
                self.game_over = True
