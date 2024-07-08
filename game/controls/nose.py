import pygame
from .base import BaseControl
from .predictions_helper import get_nose_tip

class NoseControl(BaseControl):
    def __init__(self, event):
        self.event = event

    # Data interface functions

    def predictions(self):
        preds = getattr(self.event, 'predictions', {}).get('predictions', None)

        return {
            'nose_tip': get_nose_tip(preds),
        }

    def nose_tip(self):
        return self.predictions()['nose_tip']

    def image_width(self):
        return self.event.image.shape[1] if self.event.image is not None else 1280  # Default width

    def image_height(self):
        return self.event.image.shape[0] if self.event.image is not None else 720  # Default height

    # Interpretation functions

    def nose_tilted_left(self):
        nose_tip = self.nose_tip()
        if nose_tip is None:
            return False

        # Simple condition: if nose tip is in the left half of the image
        return nose_tip['x'] < self.image_width() / 2

    def nose_tilted_right(self):
        nose_tip = self.nose_tip()
        if nose_tip is None:
            return False

        # Simple condition: if nose tip is in the right half of the image
        return nose_tip['x'] >= self.image_width() / 2

    def nose_tilted_up(self):
        nose_tip = self.nose_tip()
        if nose_tip is None:
            return False

        # Simple condition: if nose tip is in the top half of the image
        return nose_tip['y'] < self.image_height() / 2

    def nose_tilted_down(self):
        nose_tip = self.nose_tip()
        if nose_tip is None:
            return False

        # Simple condition: if nose tip is in the bottom half of the image
        return nose_tip['y'] >= self.image_height() / 2

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
