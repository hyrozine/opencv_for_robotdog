import cv2
import numpy as np

img = cv2.imread('/home/hyrozine/prs.jpg')

print(img.shape)

# getPerspectiveTransform(src, dst) get transform by 4 points
# warning : the points here are error, should be confirmed by other operation
src = np.float32([[100,100], [100, 800], [600, 100], [600, 800]])
dst = np.float32([[0, 0], [0, 800], [600, 0], [500, 600]])
M = cv2.getPerspectiveTransform(src, dst)

# cv2.warpPerspective(img, M, dsize, ...)
new = cv2.warpPerspective(img, M, (500, 600))

cv2.imshow('img', img)
cv2.imshow('new', new)
cv2.waitKey(0)
