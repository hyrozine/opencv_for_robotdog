import cv2
import numpy as np
from line_detect import line_track
import threading
import queue

class CameraThread(threading.Thread):
    def __init__(self, frame_queue):
        super().__init__()
        self.frame_queue = frame_queue
        self.capture = cv2.VideoCapture(2)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                fps = self.capture.get(cv2.CAP_PROP_FPS)
                print(fps)
                self.frame_queue.put(frame)
            else:
                print("Failed to grab frame")

    def stop(self):
        self.running = False
        self.capture.release()

class ProcessingThread(threading.Thread):
    def __init__(self, frame_queue):
        super().__init__()
        self.frame_queue = frame_queue

    def run(self):
        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                track_flag = line_track(frame)
                cv2.imshow('video',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


def main():
    frame_queue = queue.Queue(maxsize=10)

    camera_thread = CameraThread(frame_queue)
    processing_thread = ProcessingThread(frame_queue)

    camera_thread.start()
    processing_thread.start()

    try:
        while True:
            if not frame_queue.empty():
                # Optionally process frames here if needed
                pass
    except KeyboardInterrupt:
        pass
    finally:
        camera_thread.stop()
        camera_thread.join()
        processing_thread.join()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
