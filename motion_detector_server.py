from server import Server
from flask import Response
from video_feed import VideoFeed
import utils
import argparse

def create_motion_detector_server(name, port, videoFeed):
	server = Server(name, port)
	server.add_endpoint( # show the video feed on the index
		'/',
		'index',
		Response(videoFeed.webGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame'))
	return server

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Launch the motion dection server")
	parser.add_argument("--device", default="wlan0", help="todo")
	parser.add_argument("--port", type=int, default=80, help="todo")
	parser.add_argument("--video", type=int, default=0, help="todo")	
	args = parser.parse_args()

	print('PUBLIC SERVER ACCESSIBLE FROM :', utils.get_ip_address(args.device) + ':' + str(args.port))
	
	# launch the video feed
	videoFeed = VideoFeed.create(args.video)
	videoFeed.start()

	# create and run the server
	server = create_motion_detector_server(__name__, args.port, videoFeed)
	server.run()

	# close the video feed when the server is stopped
	videoFeed.close()
