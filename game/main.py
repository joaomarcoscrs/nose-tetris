import pygame
from .tetris import Tetris
from .settings import initialize_settings, SCREEN_WIDTH, SCREEN_HEIGHT, FALL_SPEED
from .colors import BLACK
from .controls import KeysControl

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
            # Change the controller being used here. It should have the same interface as BaseControl and KeysControl 
            control = KeysControl(event)
            
            if event.type == pygame.QUIT:
                running = False
            elif control.activated():
                if control.move_left() and tetris.is_valid_move(-1, 0):
                    tetris.move_shape(-1, 0)
                elif control.move_right() and tetris.is_valid_move(1, 0):
                    tetris.move_shape(1, 0)
                elif control.move_down() and tetris.is_valid_move(0, 1):
                    tetris.move_shape(0, 1)
                elif control.rotate():
                    tetris.rotate_shape()
                elif control.quit_game():
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
