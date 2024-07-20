import cv2
import numpy as np

def mouse_callback(event, x, y, flags, ueserdata):
    print(event, x, y, flags, ueserdata)

cv2.namedWindow('mouse', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mouse', 640, 360)

cv2.setMouseCallback('mouse',mouse_callback,"123")

img = np.zeros((360,640,3),np.uint8)

while True:
    cv2.imshow('mouse',img)
    key = cv2.waitKey(1)
    if key & 0xff == ord('q'):
        break

cv2.destroyWindow('mouse')