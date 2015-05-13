import socket
import time
import serial
import sys
import time
import cv2.cv as cv
import cv2
import numpy as np
import pickle
import os
import StringIO

#UDP_IP_IN = "192.168.1.245"
IP = "127.0.0.1"
PORT = 5010

receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # UDP from process over lan
receive.bind((IP, PORT))
receive.listen(10)
print 'listening'
conn, addr = receive.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])


while True:
	img_str = conn.recv(14400)
	nparr = np.fromstring(img_str[:14400], np.uint8)
        frame = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
	print type(frame)
	print sys.getsizeof(frame)
	print sys.getsizeof(img_str)
	frame2 = np.reshape(frame, (80,60,3))
	#frame3 = cv2.resize(frame2,(320,640))
	cv2.imshow('nparr', nparr)
	cv2.imshow('received',frame2)
	cv2.waitKey(10)
	time.sleep(.01)
