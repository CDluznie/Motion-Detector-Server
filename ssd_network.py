import tensorflow as tf
import numpy as np
import os

class SDDNetwork:

	def __init__(self, model_path):
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			# load the model into memory
			od_graph_def = tf.GraphDef()
			try:
				ckpt_path = os.path.join(model_path, 'frozen_inference_graph.pb')
				fid = tf.gfile.GFile(ckpt_path, 'rb')
				serialized_graph = fid.read()
				fid.close()
			except:
				raise ValueError("'" + model_path + "' is not a valid path model")
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')
			# define input and output
			self.input_network = self.detection_graph.get_tensor_by_name('image_tensor:0')
			# bounding boxes of detected objects
			self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
			# confidence in classes of detected objects
			self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
			# classes of detected objects
			self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
			# number of objects detected
			self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

	def detect_objects(self, image):
		# run the different operation on the input image
		# the image dimensions are expanded since the model expects images to have shape [1, None, None, 3]
		return self.session.run(
			[self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
			feed_dict={self.input_network: np.expand_dims(image, axis=0)})
	
	def start(self):
		# start session
		self.session = tf.Session(graph=self.detection_graph)

	def stop(self):
		# stop session
		self.session.close()

	def __enter__(self):
		self.start()
		return self

	def __exit__(self, type, value, traceback):
		self.stop()
