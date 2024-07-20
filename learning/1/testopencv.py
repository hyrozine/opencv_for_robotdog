#!/usr/bin/python3
import cv2

img = cv2.imread('/home/hyrozine/test_pic.jpg')

cv2.imshow('img',img) 

key = cv2.waitKey(0)

if(key & 0xff == ord('q')):   # ord() -> get the ASCII of 'q' 
    cv2.destroyAllWindows()






