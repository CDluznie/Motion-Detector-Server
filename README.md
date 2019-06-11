# Motion-Detector-Server

A simple Flask server to create intelligent surveillance camera.
The server is accessible from any devices on local network at the given IP address on launch.

When the server start, it connect to the video peripheral to capture a reference frame.
After this stage, the server will check the video stream if there is a noticeable difference between the current frame and the reference frame.
So the process work only if the camera is static.

## Requirements

* Flask
* OpenCV

See *requirements.txt* for all dependences

## Usage

* Install dependences : pip install -r requirements.txt
* Run : `motion_detector_server.py [--networkDevice NetworkDevice] [--port Port] [--videoDevice VideoDevice]`
    * *networkDevice* : name of Wi-Fi card (default *wlan0*)
    * *port* : port of the server (default *80*)
    * *videoDevice* : index of video device to use (default *0*)
