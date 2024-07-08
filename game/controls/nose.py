import pygame

from .base import BaseControl

class NoseControl(BaseControl):
    def __init__(self, event):
        self.event = event
    
    def predictions(self):
        result = getattr(self.event, 'predictions', {})
        
        print(result['predictions'])
        
        return result['predictions']

    def activated(self):
        return self.event.type == pygame.USEREVENT and self.event.predictions is not None

    def move_left(self):
        for prediction in self.predictions():
            if prediction['class'] == 'eye-axis':
                left_eye = prediction['keypoints'][0]
                right_eye = prediction['keypoints'][1]
                nose_x = (left_eye['x'] + right_eye['x']) / 2
                image_width = 1280  # You can dynamically get this value from predictions if needed
                if nose_x < image_width / 2 - 50:  # Adjust the threshold as needed
                    return True
        return False
    
    def move_right(self):
        for prediction in self.predictions():
            if prediction['class'] == 'eye-axis':
                left_eye = prediction['keypoints'][0]
                right_eye = prediction['keypoints'][1]
                nose_x = (left_eye['x'] + right_eye['x']) / 2
                image_width = 1280  # You can dynamically get this value from predictions if needed
                if nose_x > image_width / 2 + 50:  # Adjust the threshold as needed
                    return True
        return False

    def move_down(self):
        for prediction in self.predictions():
            if prediction['class'] == 'eye-axis':
                left_eye = prediction['keypoints'][0]
                right_eye = prediction['keypoints'][1]
                nose_y = (left_eye['y'] + right_eye['y']) / 2
                image_height = 720  # You can dynamically get this value from predictions if needed
                if nose_y > image_height / 2 + 50:  # Adjust the threshold as needed
                    return True
        return False
    
    def rotate(self):
        for prediction in self.predictions():
            if prediction['class'] == 'eye-axis':
                left_eye = prediction['keypoints'][0]
                right_eye = prediction['keypoints'][1]
                nose_y = (left_eye['y'] + right_eye['y']) / 2
                image_height = 720  # You can dynamically get this value from predictions if needed
                if nose_y < image_height / 2 - 50:  # Adjust the threshold as needed
                    return True
        return False

    def quit_game(self):
        return False  # No quit game action for nose control, modify as needed
