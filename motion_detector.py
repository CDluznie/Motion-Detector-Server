from ssd_network import SDDNetwork
from tf_utils import label_map_util
from tf_utils import visualization_utils as vis_utils
import cv2
import numpy as np
import imutils

class MotionDetector:

	def __init__(self, ssd_detector, category_index):
		self.ssd_detector = ssd_detector
		self.category_index = category_index

	@staticmethod
	def create(firstImg, modelPath='model/ssd_mobilenet_v1_coco_2017_11_17', labelsPath='model/data/mscoco_label_map.pbtxt'):
		ssd_detector = SDDNetwork(modelPath)
		category_index = label_map_util.create_category_index_from_labelmap(labelsPath, use_display_name=True)
		ssd_detector.start()
		return MotionDetector(ssd_detector, category_index)
		
	def detect(self, img, width=500):
		frame = imutils.resize(img, width=width)
		"""
		(boxes, scores, classes, number_detected) = self.ssd_detector.detect_objects(frame)
		# TODO display only person, cat, dog
		vis_utils.visualize_boxes_and_labels_on_image_array(
			frame,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=8)
		"""
		return frame


	# TODO close
	# ssd_detector.stop()
