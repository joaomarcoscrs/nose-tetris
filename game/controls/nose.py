import pygame

from .base import BaseControl
from .predictions_helper import get_left_eye, get_right_eye, get_nose_top, get_nose_bottom, get_nose_tip



class NoseControl(BaseControl):
    def __init__(self, event):
        self.event = event
    
    # Data interface functions
    
    def predictions(self):
        preds = getattr(self.event, 'predictions', {}).get('predictions', None)
        
        return {
            'nose_top': get_nose_top(preds),
            'nose_bottom': get_nose_bottom(preds),
            'nose_tip': get_nose_tip(preds),
            'left_eye': get_left_eye(preds),
            'right_eye': get_right_eye(preds),
        }
    
    def nose_top(self):
        return self.predictions()['nose_top']
    
    def nose_bottom(self):
        return self.predictions()['nose_bottom']
    
    def nose_tip(self):
        return self.predictions()['nose_tip']
    
    def left_eye(self):
        return self.predictions()['left_eye']
    
    def right_eye(self):
        return self.predictions()['right_eye']

    def eye_midpoint(self):
        left_eye = self.left_eye()
        right_eye = self.right_eye()
        
        if left_eye is None or right_eye is None:
            return None
        
        return {
            'x': (left_eye['x'] + right_eye['x']) / 2,
            'y': (left_eye['y'] + right_eye['y']) / 2
        }
    
    # Interpretation functions
    
    def nose_tilted_up(self):
        CLOSE_TO_EYES_THRESHOLD = 50
        
        nose_tip = self.nose_tip()
        eye_midpoint = self.eye_midpoint()
        
        if nose_tip is None or eye_midpoint is None:
            return False

        return nose_tip['y'] - eye_midpoint['y'] < CLOSE_TO_EYES_THRESHOLD
    
    def nose_tilted_down(self):
        CLOSE_TO_NOSE_BOTTOM_THRESHOLD = 10
        
        nose_tip = self.nose_tip()
        nose_bottom = self.nose_bottom()
        
        if nose_tip is None or nose_bottom is None:
            return False
        
        return nose_bottom['y'] - nose_tip['y'] < CLOSE_TO_NOSE_BOTTOM_THRESHOLD
    
    def nose_tilted_left(self):
        CLOSE_TO_LEFT_EYE_THRESHOLD = 50
        
        nose_tip = self.nose_tip()
        left_eye = self.left_eye()
        
        print('debug nose tilted left', 'nose_tip', nose_tip, 'left_eye', left_eye)
        
        if left_eye is not None and nose_tip is not None:
            return left_eye['x'] - nose_tip['x'] < CLOSE_TO_LEFT_EYE_THRESHOLD

        if nose_tip is not None:
            # nose tip is more to the left than the nose top
            return nose_tip['x'] - self.nose_top()['x'] < CLOSE_TO_LEFT_EYE_THRESHOLD
        
        return False
    
    def nose_tilted_right(self):
        CLOSE_TO_RIGHT_EYE_THRESHOLD = 50
        
        nose_tip = self.nose_tip()
        right_eye = self.right_eye()
    
        if right_eye is not None and nose_tip is not None:
            return nose_tip['x'] - right_eye['x'] < CLOSE_TO_RIGHT_EYE_THRESHOLD
        
        if nose_tip is not None:
            # nose tip is more to the right than the nose top
            return self.nose_top()['x'] - nose_tip['x'] < CLOSE_TO_RIGHT_EYE_THRESHOLD

    # Control functions
    
    def activated(self):
        return self.event.type == pygame.USEREVENT and self.event.predictions is not None

    def move_left(self):
        return self.nose_tilted_left()
    
    def move_right(self):
        return self.nose_tilted_right()

    def move_down(self):
        return self.nose_tilted_down()
    
    def rotate(self):
        return self.nose_tilted_up()

    def quit_game(self):
        return False  # No quit game action for nose control
