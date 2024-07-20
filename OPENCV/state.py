import cv2
from utils import COLOR, STATE

class State_Machine():
    def __init__(self):
        self.state = STATE['state_recognize_ball']
        #self.state = STATE['state_3_yellow_climb']
        self.ball_time = 0
        self.now_time = 0
        self.yellow_time = 0
        self.bucket_time = 0



state_machine = State_Machine()
