from server import Server
from video_feed import VideoFeed
import atexit
import utils

def create_motion_detector_server(name, videoFeed):
	server = Server(name)
	server.add_endpoint(
		'/',
		'index',
		Response(videoFeed.webGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame'))
	return server

if __name__ == '__main__':

        # todo args

	device = 'wlan0'	
	port = 80

	print('PUBLIC SERVER ACCESSIBLE FROM :', utils.get_ip_address(device) + ':' + str(port))
	
	# launch the video feed
	videoFeed = VideoFeed.create(1)
	videoFeed.start()

	# create and run the server
	server = create_motion_detector_server(__name__, videoFeed)
	server.run()

	# stop the video feed when the server is stopped
	videoFeed.close()
