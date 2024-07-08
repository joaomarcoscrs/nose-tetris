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

    def image_width(self):
        return self.event.image.shape[1] if self.event.image is not None else 1280  # Default width

    def image_height(self):
        return self.event.image.shape[0] if self.event.image is not None else 720  # Default height
    
    def eye_axis_length(self):
        left_eye = self.left_eye()
        right_eye = self.right_eye()

        if left_eye is None or right_eye is None:
            return 0

        return abs(left_eye['x'] - right_eye['x'])

    def nose_axis_length(self):
        nose_top = self.nose_top()
        nose_bottom = self.nose_bottom()

        if nose_top is None or nose_bottom is None:
            return 0

        return abs(nose_top['y'] - nose_bottom['y'])

    # Interpretation functions
    
    def nose_horizontal_tilt_threshold(self):
        eye_axis_length = self.eye_axis_length()
        
        if eye_axis_length != 0:
            return eye_axis_length * 0.2
        
        return self.image_width() * 0.1
    
    def nose_vertical_tilt_threshold(self):
        nose_axis_length = self.nose_axis_length()
        
        if nose_axis_length != 0:
            return nose_axis_length * 0.3
        
        return self.image_height() * 0.2

    def nose_tilted_up(self):
        nose_tip = self.nose_tip()
        eye_midpoint = self.eye_midpoint()

        if nose_tip is not None and eye_midpoint is not None:
            return nose_tip['y'] - eye_midpoint['y'] < self.nose_vertical_tilt_threshold()
        
        if nose_tip is not None:
            return nose_tip['y'] < self.image_height() * 0.2

    def nose_tilted_down(self):
        nose_bottom = self.nose_bottom()
        eye_midpoint = self.eye_midpoint()
        
        if nose_bottom is not None and eye_midpoint is not None:
            return eye_midpoint['y'] - nose_bottom['y'] < self.nose_vertical_tilt_threshold()
        
        if nose_bottom is not None:
            return nose_bottom['y'] > self.image_height() * 0.8

    def nose_tilted_left(self):
        nose_tip = self.nose_tip()
        left_eye = self.left_eye()

        if left_eye is not None and nose_tip is not None:
            return left_eye['x'] - nose_tip['x'] < self.nose_horizontal_tilt_threshold()
        
        if nose_tip is not None:
            # nose tip is more to the left than the nose top
            return nose_tip['x'] - self.nose_top()['x'] < self.nose_horizontal_tilt_threshold()
        return False

    def nose_tilted_right(self):
        nose_tip = self.nose_tip()
        right_eye = self.right_eye()

        if right_eye is not None and nose_tip is not None:
            return nose_tip['x'] - right_eye['x'] < self.nose_horizontal_tilt_threshold()
        
        if nose_tip is not None:
            # nose tip is more to the right than the nose top
            return self.nose_top()['x'] - nose_tip['x'] < self.nose_horizontal_tilt_threshold()
        return False

    # Control functions

    def activated(self):
        return self.event.type == pygame.USEREVENT and self.event.predictions is not None

    def move_left(self):
        return self.nose_tilted_right()

    def move_right(self):
        return self.nose_tilted_left()

    def move_down(self):
        return self.nose_tilted_down()

    def rotate(self):
        return self.nose_tilted_up()

    def quit_game(self):
        return False  # No quit game action for nose control
