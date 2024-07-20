import cv2
import numpy as np



def center(x, y, w, h):
    x1 = int(x/2)
    y1 = int(y/2)
    cx = int(w/2)
    cy = int(h/2)
    return x1, y1

min_w = 70
min_h = 70
line_height = 200
cars = []
carnum = 0
offset = 6


cap = cv2.VideoCapture('/home/hyrozine/cars.mp4')

# bgsubmog = cv2.createBackgroundSubtractorMOG2()
bgsubmog = cv2.createBackgroundSubtractorKNN()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

while True:
    ret,frame = cap.read()

    if(ret == True):
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(frame, (3,3),5)
        mask = bgsubmog.apply(blur)

        # Remove the small patches in the figure
        erode = cv2.erode(mask, kernel)
        # recover the reduction
        dilate = cv2.dilate(erode, kernel,iterations = 2)
        # remove the hole in the cars
        close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE,kernel)
        # close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE,kernel)

        cnts, hietarchy = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.line(frame, (10, line_height), (1200, line_height), (255,255,0), 2)

        for(i,c) in enumerate(cnts):
            x,y,w,h = cv2.boundingRect(c)
            # check if it is a real car
            isValid = ( w >= min_w) and (h >= min_h)
            if(not isValid):
                continue
            
            # frame selected veichle 
            cv2.rectangle(frame, (x,y),(x+w, y+h),(0,0,255),2)
            
            cpoints = center(x, y, w, h)
            cars.append(cpoints)

            for (x,y) in cars:
                if((y > line_height - offset) and (y < line_height + offset)):
                    carnum += 1
                    cars.remove((x, y))
                    print(carnum)

        cv2.putText(frame, "Cars Count:"+ str(carnum), (500,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0) ,5)
        # cv2.imshow('video',mask)
        # cv2.imshow('erode',erode)
        # cv2.imshow('dilate',dilate)
        # cv2.imshow('close',close)
        cv2.imshow('video',frame)

    key = cv2.waitKey(100)
    if(key == 27):
        break

cap.release
cv2.destroyAllWindows()