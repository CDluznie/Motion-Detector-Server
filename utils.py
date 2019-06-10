import cv2
import socket
import fcntl
import struct

def imageToBytes(img):
    _,bytes = cv2.imencode('.jpeg', img)
    return bytearray(bytes)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', str.encode(ifname[:15]))
    )[20:24])
