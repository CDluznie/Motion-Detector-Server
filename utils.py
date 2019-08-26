import cv2
import socket
import os
import fcntl
import struct

def imageToBytes(img):
	_,bytes = cv2.imencode('.jpeg', img)
	return bytearray(bytes)

def get_ip_address_old(ifname): # TODO remove
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', str.encode(ifname[:15]))
    )[20:24])

def get_ip_address():
	gw = os.popen("ip -4 route show default").read().split()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((gw[2], 0))
	ipaddr = s.getsockname()[0]
	return ipaddr

