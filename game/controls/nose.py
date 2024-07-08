import pygame
from .base import BaseControl
from .predictions_helper import get_nose_top, get_nose_bottom, get_nose_tip

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
        }

    def nose_top(self):
        return self.predictions()['nose_top']

    def nose_bottom(self):
        return self.predictions()['nose_bottom']

    def nose_tip(self):
        return self.predictions()['nose_tip']

    def image_width(self):
        return self.event.image.shape[1] if self.event.image is not None else 1280  # Default width

    def image_height(self):
        return self.event.image.shape[0] if self.event.image is not None else 720  # Default height

    # Interpretation functions

    def nose_tilted_left(self):
        nose_tip = self.nose_tip()
        nose_top = self.nose_top()
        nose_bottom = self.nose_bottom()

        if nose_tip is None or nose_top is None or nose_bottom is None:
            return False

        # If the nose tip is more to the left than both the nose top and nose bottom
        return nose_tip['x'] < nose_top['x'] and nose_tip['x'] < nose_bottom['x']

    def nose_tilted_right(self):
        nose_tip = self.nose_tip()
        nose_top = self.nose_top()
        nose_bottom = self.nose_bottom()

        if nose_tip is None or nose_top is None or nose_bottom is None:
            return False

        # If the nose tip is more to the right than both the nose top and nose bottom
        return nose_tip['x'] > nose_top['x'] and nose_tip['x'] > nose_bottom['x']

    def nose_tilted_up(self):
        nose_tip = self.nose_tip()
        eye_midpoint = {'y': self.image_height() / 2}  # Using the midpoint of the image height for simplicity

        if nose_tip is not None:
            return nose_tip['y'] < eye_midpoint['y']

    def nose_tilted_down(self):
        nose_tip = self.nose_tip()
        eye_midpoint = {'y': self.image_height() / 2}  # Using the midpoint of the image height for simplicity

        if nose_tip is not None:
            return nose_tip['y'] >= eye_midpoint['y']

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
