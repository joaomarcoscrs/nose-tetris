import pygame

from .base import BaseControl

class KeysControl(BaseControl):
    def activated(self):
        return self.event.type == pygame.KEYDOWN
      
    def move_left(self):
        return self.event.key == pygame.K_LEFT
    
    def move_right(self):
        return self.event.key == pygame.K_RIGHT
    
    def move_down(self):
        return self.event.key == pygame.K_DOWN
    
    def rotate(self):
        return self.event.key == pygame.K_UP
    
    def quit_game(self):
        return self.event.key == pygame.K_ESCAPE