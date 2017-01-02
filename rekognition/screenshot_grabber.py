import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from config_handler import config
import datetime
from multiprocessing.pool import ThreadPool
import threading
from queue import Queue, Empty
import mqtt_client

take_screenshot = False

class ScreenshotGrabber(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.tmp_folder = config.get('rekognition', 'tmp_folder', fallback='')
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        self.frames_without_faces = -1
        self.new_face_detected_start = -1

        self.cascPath = self.dirname + '/haarcascade_frontalface_default.xml'
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.mqttc = mqtt_client.MQTT_Client(name='ScreenshotGrabberSub')

    def check_video_capture(self):
        self.video_capture = cv2.VideoCapture(0)
        if self.video_capture.isOpened():  # try to get the first frame
            rval, frame = self.video_capture.read()
        else:
            rval = False
        return rval

    def count_frames_without_faces(self, faces):
        if len(faces) == 0:
            self.frames_without_faces = self.frames_without_faces + 1
            print(self.frames_without_faces)
        else:
            if self.frames_without_faces > 20:
                self.new_face_detected_start = 0
            self.frames_without_faces = 0
        return

    def screenshot_delay_counter(self):
        global take_screenshot
        if self.new_face_detected_start > - 1:
            self.new_face_detected_start = self.new_face_detected_start + 1
        if self.new_face_detected_start == 5:
            self.new_face_detected_start = -1
            take_screenshot = True
        return

    def grab_screenshot(self, frame, force_screenshot=False):
        global take_screenshot
        if take_screenshot or force_screenshot:
            take_screenshot = False
            now_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
            screenshot = '%s%s_%s.jpg' % (self.tmp_folder, 'screenshot', now_str)
            print('Taking screenshot...')
            cv2.imwrite(screenshot, frame)  # save image
        return

    def force_screenshot(self):
        global take_screenshot
        take_screenshot = True
        return

    def key_grabber(self):
        global take_screenshot
        key = cv2.waitKey(20)
        # print(key)
        if key == 1048691:  # 's' screenshot
            take_screenshot = True
        return key

    def capture_video(self):
        global take_screenshot
        rval  = self.check_video_capture()
        while rval:
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Detect if at least one face is detected
            self.count_frames_without_faces(faces)

            # Wait x frames after new face is detected to take the screenshot
            self.screenshot_delay_counter()
            self.grab_screenshot(frame)

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            key = self.key_grabber()
            if key == 1048603:  # exit on ESC
                break

        self.release_capture()
        return

    def release_capture(self):
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

    def run(self):
        self.capture_video()

if __name__ == "__main__":
    screenshot_grabber = ScreenshotGrabber()
    screenshot_grabber.start()
