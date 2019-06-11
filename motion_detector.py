import cv2
import numpy as np
import imutils
import datetime

class MotionDetector:

	def __init__(self, referenceFrame, threshold, minArea):
		self.referenceFrame = referenceFrame
		self.threshold = threshold
		self.minArea = minArea

	@staticmethod
	def create(firstImg, threshold=45, morphoMathKernelSize=9, minArea=500):
		referenceFrame = MotionDetector.__toGrayImage(MotionDetector.__resizeImage(firstImg))
		return MotionDetector(referenceFrame, threshold, minArea)
		
	def detect(self, img):
		frame = MotionDetector.__resizeImage(img)
		gray = MotionDetector.__toGrayImage(frame)
		# compute the zone where there is a difference between the current frame and the reference frame
		diff = cv2.absdiff(self.referenceFrame, gray)
		_,thresh = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
		kernel = np.ones((morphoMathKernelSize,morphoMathKernelSize),np.uint8)
		objects = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		# extact the contours of the objects
		cnts = [
			cnt 
			for cnt in imutils.grab_contours(cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)) 
			if cv2.contourArea(cnt) > self.minArea
		]
		# draw targets and texts
		text = "Detected" if len(cnts) > 0 else "None"
		textColor = (0, 0, 255)
		MotionDetector.__drawTargets(frame, cnts)
		cv2.putText(frame, "Targets: {}".format(text), (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, textColor, 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (6, frame.shape[0] - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, textColor, 1)
		return frame

	@staticmethod
	def __resizeImage(img, width=500):
		return imutils.resize(img, width=width)

	@staticmethod
	def __toGrayImage(img, gaussianKernel=(21, 21)):
		return cv2.cvtColor(cv2.GaussianBlur(img, gaussianKernel, 0), cv2.COLOR_BGR2GRAY)

	@staticmethod
	def __drawTargets(frame, contours, color=(0, 255, 0)):
		for contour in contours:
			x, y, w, h = cv2.boundingRect(contour)
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

	
