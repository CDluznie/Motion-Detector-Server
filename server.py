from flask import Flask, Response
from video_feed import VideoFeed
import atexit
import utils

videoFeed = VideoFeed.create(1)
atexit.register(videoFeed.close)
videoFeed.start()

app = Flask(__name__)

@app.route('/')
def videoFeedWeb():
	return Response(videoFeed.webGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

        # todo args

	device = 'wlan0'	
	port = 80

	print('PUBLIC SERVER ACCESSIBLE FROM :', utils.get_ip_address(device) + ':' + str(port))

	app.run(host='0.0.0.0', port=80)
