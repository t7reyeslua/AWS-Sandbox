import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from config_handler import config
import datetime

take_screenshot = False
tmp_folder = config.get('rekognition', 'tmp_folder', fallback='')
dirname = os.path.dirname(os.path.realpath(__file__))
frames_without_faces = -1
new_face_detected_start = -1

cascPath = dirname + '/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
if video_capture.isOpened(): # try to get the first frame
    rval, frame = video_capture.read()
else:
    rval = False

while rval:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Detect if at least one face is detected
    if len(faces) == 0:
        frames_without_faces = frames_without_faces + 1
        print(frames_without_faces)
    else:
        if frames_without_faces > 20:
            new_face_detected_start = 0
        frames_without_faces = 0

    # Wait x frames after new face is detected to take the screenshot
    if new_face_detected_start > - 1:
        new_face_detected_start = new_face_detected_start + 1
    if new_face_detected_start == 5:
        new_face_detected_start = -1
        take_screenshot = True

    if take_screenshot:
        take_screenshot = False
        now_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S')
        screenshot = '%s%s_%s.jpg' % (tmp_folder, 'screenshot', now_str)
        cv2.imwrite(screenshot, frame)  # save image

    # Display the resulting frame
    cv2.imshow('Video', frame)

    key = cv2.waitKey(20)
    # print(key)
    if key == 1048603:  # exit on ESC
        break
    elif key == 1048691:  # 's' screenshot
        take_screenshot = True

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
