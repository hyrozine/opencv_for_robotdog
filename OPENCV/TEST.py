import cv2
import numpy as np
from utils import COLOR_THRESHOLD
import color_detect
import ball_detect

path = '/home/hyrozine/imgs/orange.jpg'

img = cv2.imread(path)

ball_detect.detect_ball(img, 'ORANGE')