import cv2
import threading
import utils
from motion_detector import MotionDetector

class ReadWriteValue:

    def __init__(self):
        self.lock = threading.Lock()
        self.isUpdated = False

    def set(self, value):
        with self.lock:
            self.value = value
        self.isUpdated = False

    def get(self):
        if not self.isUpdated:
            with self.lock:
                self.cachedValue = self.value
            self.isUpdated = True
        return self.cachedValue

class VideoFeed:

    def __init__(self, capture, detector):
        self.capture = capture
        self.detector = detector
        self.currentFrame = ReadWriteValue()
        self.threadCaptureReader = threading.Thread(target=self.__threadReadCapture)
        self.isReading = True

    @staticmethod
    def create(videoSrc, indexFrame=30):
        capture = cv2.VideoCapture(videoSrc)
	# we can't take the first frame of the capture
	# because the video peripheral may be need some initialization to produce acceptable frame
        for _ in range(indexFrame): # Iterate 
            isOpen, firstImg = capture.read()
            if not isOpen:
                raise IOError("video stream '" + str(videoSrc) + "' is not readable")
        motionDetector = MotionDetector.create(firstImg)
        return VideoFeed(capture, motionDetector)

    def start(self):
        self.threadCaptureReader.start()

    def close(self):
        self.isReading = False
        self.threadCaptureReader.join()
        self.capture.release()
    
    def webGenerator(self):
        while True: # todo isReading
            img = self.currentFrame.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

    def __threadReadCapture(self):
        while self.isReading:
            isOpen, img = self.capture.read()
            if not isOpen:
                continue
            processedImg = self.detector.detect(img)
            self.currentFrame.set(utils.imageToBytes(processedImg))

