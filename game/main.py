import pygame
import threading

from .tetris import Tetris
from .settings import initialize_settings, SCREEN_WIDTH, SCREEN_HEIGHT, FALL_SPEED
from .colors import BLACK
from .controls import KeysControl, NoseControl
from .roboflow import main as inference_main

from typing import Union
from .roboflow import VideoFrame

# Initialize Pygame
pygame.init()

# Initialize settings
SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE = initialize_settings()

# Initialize screen in full screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')

# Clock
clock = pygame.time.Clock()

EVENT_TIMEOUT = 100

LAST_EVENT_TIME = 0

def post_predictions_event(predictions: dict, image: Union[None, VideoFrame]):
    global LAST_EVENT_TIME
    global EVENT_TIMEOUT
    # Only posts 1 event every EVENT_TIMEOUT ms
    
    if pygame.time.get_ticks() - LAST_EVENT_TIME < EVENT_TIMEOUT:
        return
      
    LAST_EVENT_TIME = pygame.time.get_ticks()
    
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {
        'user_type': 'predictions',
        'predictions': predictions,
        'image': image
    }))

def game_main():
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
            controls = [KeysControl(event), NoseControl(event)]
            
            for control in controls:
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

def run_game():
    threading.Thread(target=inference_main, args=(post_predictions_event,), daemon=True).start()
    game_main()

if __name__ == '__main__':
    run_game()
