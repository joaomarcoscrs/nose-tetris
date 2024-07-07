import pygame
from .tetris import Tetris
from .settings import initialize_settings, SCREEN_WIDTH, SCREEN_HEIGHT, FALL_SPEED
from .colors import BLACK

# Initialize Pygame
pygame.init()

# Initialize settings
SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE = initialize_settings()

# Initialize screen in full screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')

# Clock
clock = pygame.time.Clock()

def main():
    tetris = Tetris()
    fall_time = 0

    running = True
    while running:
        screen.fill(BLACK)
        tetris.draw_grid(screen)
        tetris.draw_shape(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetris.is_valid_move(-1, 0):
                    tetris.move_shape(-1, 0)
                elif event.key == pygame.K_RIGHT and tetris.is_valid_move(1, 0):
                    tetris.move_shape(1, 0)
                elif event.key == pygame.K_DOWN and tetris.is_valid_move(0, 1):
                    tetris.move_shape(0, 1)
                elif event.key == pygame.K_UP:
                    tetris.rotate_shape()
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Exit full screen mode on pressing ESC

        fall_time += clock.get_time()
        if fall_time > FALL_SPEED:
            tetris.update()
            fall_time = 0

        if tetris.game_over:
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
