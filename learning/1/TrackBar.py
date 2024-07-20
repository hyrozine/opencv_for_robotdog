import cv2
import numpy as np
def callback():
    pass


cv2.namedWindow('trackbar')

# create trackbar
cv2.createTrackbar('R','trackbar',0,255,callback)
cv2.createTrackbar('G','trackbar',0,255,callback)
cv2.createTrackbar('B','trackbar',0,255,callback)

# create a backgroud picture
img = np.zeros((480,460,3), np.uint8)

while True:
    # get the trackbar value
    r = cv2.getTrackbarPos('R','trackbar')
    g = cv2.getTrackbarPos('G','trackbar')
    b = cv2.getTrackbarPos('B','trackbar')

    # change the value
    img[:] = [b,g,r]
    cv2.imshow('trackbar',img)

    key = cv2.waitKey(10)
    if key & 0xff == ord('q'):
        break

cv2.destroyAllWindows()