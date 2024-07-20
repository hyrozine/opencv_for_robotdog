import cv2
import numpy as np

# use mouse to graph
# press 'l' for lines, 'r' for rectangle, 'c' for circle.
cv2.namedWindow('graph', cv2.WINDOW_NORMAL)

cur_shape = 0
startpoint = (0,0)
img = np.zeros((480,640,3),np.uint8)

def mouse_callback(event, x, y, flags, cur_shape):
    #print(event, x, y, flags, ueserdata)
    global startpoint
    if (event & cv2.EVENT_LBUTTONDOWN == cv2.EVENT_LBUTTONDOWN):
        startpoint = (x,y)
    elif(event & cv2.EVENT_LBUTTONUP == cv2.EVENT_LBUTTONUP):
        if cur_shape == 0:
            cv2.line(img, startpoint, (x,y), (0, 0, 255))
        elif cur_shape == 1:
            cv2.rectangle(img, startpoint, (x,y), (255,0,0))
        elif cur_shape == 2:
            a = (x - startpoint[0])
            b = (y - startpoint[1])
            r = int((a**2+b**2)**0.5)
            cv2.circle(img, startpoint, r, (0, 255, 0))
        else:
            print("error: invalid input.")


while True:
    cv2.imshow('graph',img)
    key = cv2.waitKey(1) & 0xff 
    if key == ord('q'):
        break
    elif key == ord('l'): # line
        cur_shape = 0
    elif key == ord('r'): # rectangle
        cur_shape = 1
    elif key == ord('c'): # circlea
        cur_shape = 2
    cv2.setMouseCallback('graph',mouse_callback,cur_shape)

cv2.destroyWindow('graph')