import imutils
import cv2

class ObjCenter:
    def __init__(self, haarPath):
        self.detector = cv2.CascadeClassifier(haarPath)

    def find_center(self, frame, frameCenter):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # find all objects we are interested in
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.05,
                                               minNeighbors=9, minSize=(30,30),
                                               flags=cv2.CASCADE_SCALE_IMAGE)

        # check if an object was found
        if len(rects) > 0:
            x, y, w, h = rects[0]
            center_x = int(x + (w / 2.0))
            center_y = int(y + (h / 2.0))

            return ((center_x, center_y), rects[0])

        # return frame center if no objects found
        return (frameCenter, None)
