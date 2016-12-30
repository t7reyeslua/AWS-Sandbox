import cv2
import sys
import os

dirname = os.path.dirname(os.path.realpath(__file__))
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

    # Display the resulting frame
    cv2.imshow('Video', frame)

    key = cv2.waitKey(20)
    # print(key)
    if key == 1048603:  # exit on ESC
        break
    elif key == 1048691:  # 's' screenshot
        pass

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
