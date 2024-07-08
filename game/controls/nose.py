import pygame
from .base import BaseControl
from .predictions_helper import get_nose_top, get_nose_bottom, get_nose_tip, get_left_eye, get_right_eye

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
        nose_top = self.nose_top()
        nose_bottom = self.nose_bottom()
        eye_midpoint = self.eye_midpoint()

        if nose_tip is None and nose_bottom is None:
            return False

        close_threshold = self.image_height() * 0.1  # 20% of the image height

        # If the nose tip is close to the nose top
        if nose_tip and nose_top and abs(nose_tip['y'] - nose_top['y']) < close_threshold:
            return True

        # If the nose tip is close to the y-coordinate of the eyes' midpoint
        if nose_tip and abs(nose_tip['y'] - eye_midpoint['y']) < close_threshold:
            return True

        # If only the nose bottom is visible and it's close to the eyes' midpoint
        if nose_bottom and abs(nose_bottom['y'] - eye_midpoint['y']) < close_threshold:
            return True

        # If the nose bottom is close to the nose top
        if nose_bottom and nose_top and abs(nose_bottom['y'] - nose_top['y']) < close_threshold:
            return True

        # If the length of the nose axis is significantly shorter than the length of the eye axis
        eye_axis_length = self.eye_axis_length()
        nose_axis_length = self.nose_axis_length()
        if eye_axis_length and nose_axis_length and nose_axis_length < eye_axis_length * 0.5:
            return True

        return False

    def nose_tilted_down(self):
        nose_tip = self.nose_tip()
        eye_midpoint = {'y': self.image_height() / 2}  # Using the midpoint of the image height for simplicity

        if nose_tip is not None:
            return nose_tip['y'] >= eye_midpoint['y']

    # Control functions

    def activated(self):
        return self.event.type == pygame.USEREVENT and self.event.predictions is not None

    def move_left(self):
        return self.nose_tilted_right()  # Corrected to match webcam reflection

    def move_right(self):
        return self.nose_tilted_left()  # Corrected to match webcam reflection

    def move_down(self):
        return self.nose_tilted_down()

    def rotate(self):
        return self.nose_tilted_up()

    def quit_game(self):
        return False  # No quit game action for nose control
