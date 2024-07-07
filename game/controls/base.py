class BaseControl:
    def __init__(self, event):
        self.event = event

    def quit_game(self):
        raise NotImplementedError
        
    def move_left(self):
        raise NotImplementedError
      
    def move_right(self):
        raise NotImplementedError
      
    def move_down(self):
        raise NotImplementedError
      
    def rotate(self):
        raise NotImplementedError