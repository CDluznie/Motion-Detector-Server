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
		
	def detect(self, img, width=500, targets={'person', 'dog', 'cat'}):
		frame = imutils.resize(img, width=width)
		(boxes, scores, classes, number_detected) = self.ssd_detector.detect_objects(frame)
		boxes = np.squeeze(boxes)
		scores = np.squeeze(scores)
		classes = np.squeeze(classes).astype(np.int32)
		# get the id of only desired classes		
		targets_id = {i for i,val in self.category_index.items() if val['name'] in targets}
		targets_indices = np.argwhere(np.logical_or.reduce([
			classes == target_id for target_id in targets_id
		]))
		# draw the result on the frame
		vis_utils.visualize_boxes_and_labels_on_image_array(
			frame,
			np.squeeze(boxes[targets_indices]),
			np.squeeze(classes[targets_indices]),
			np.squeeze(scores[targets_indices]),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=8)
		return frame


	# TODO close
	# ssd_detector.stop()
