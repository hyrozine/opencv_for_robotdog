import cv2
import numpy as np

#               (y , x)
img = np.zeros((480,640,3),np.uint8)

# draw lines.  (x,y)                           width shape   shape = -1,4,8,16
cv2.line(img, (10,20), (50 , 500), (120,220,230), 5,  4)
cv2.line(img, (50,50), (340 , 500), (0, 0, 230), 5,  16)

# draw retangles 
cv2.rectangle(img,(10,10),(200,100),(0,0,255),-1)

# draw circles
cv2.circle(img,(320,230),100,(0,0,255))
cv2.circle(img,(320,230),5,(0,0,255),-1)


# draw ellipses
#                  pos       a,b  angle  range
# the range increase clockwise
# the angle represents how much the ellipse rotates clockwise
cv2.ellipse(img, (320,420),(100,50), 0, 50, 360, (0, 0, 255))

# draw polylines
pts = np.array([(300,10),(150,100),(450,100)],np.int32)
#              point set|connect or not
cv2.polylines(img, [pts], True, (0,0,255))
# fill the polygon
cv2.fillPoly(img,[pts],(255,255,0))

# draw texts
cv2.putText(img,"hello world", (100, 400), cv2.FONT_HERSHEY_TRIPLEX,2,(0,255,0))

cv2.imshow('draw',img)
cv2.waitKey(0)