import pygame
import random
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE
from .colors import WHITE, SHAPE_COLORS
from .shapes import SHAPES

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_shape = self.get_new_shape()
        self.current_color = random.choice(SHAPE_COLORS)
        self.shape_x = 3
        self.shape_y = 0
        self.game_over = False

    def get_new_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self, screen):
        for y in range(20):
            for x in range(10):
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_shape(self, screen):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, self.current_color, ((self.shape_x + x) * GRID_SIZE, (self.shape_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

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
        while len(new_grid) < 20:
            new_grid.insert(0, [0 for _ in range(10)])
        self.grid = new_grid

    def is_valid_move(self, dx, dy):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or self.grid[new_y][new_x] != 0:
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
