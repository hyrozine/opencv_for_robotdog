import cv2
import ball_detect

img_size = (640, 480)

cv2.namedWindow('video',cv2.WINDOW_AUTOSIZE)
# cv2.resizeWindow('video',640,480)

if __name__ == '__main__':
    video = cv2.VideoCapture('/home/hyrozine/Videos/orange_video.mp4')
    # video.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    # video.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    # video.set(cv2.CAP_PROP_FPS, 30)
    while video.isOpened():
        ret,frame = video.read()
        if frame is None:
            break
        if ret == True:
            # _, result = ball_detect.detect_ball(frame, 'ORANGE')
            cv2.imshow('video',frame)
            key = cv2.waitKey(1)
            if(key & 0xFF == ord('q')) :
                break
video.release()
cv2.destroyAllWindows()