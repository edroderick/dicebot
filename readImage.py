import numpy as np
import cv2
import time
from cv2 import cv
import socket
import sys


if __name__ == "__main__":
## ---------- UDP Start ---------------
      UDP_IP = "127.0.0.1"
      UDP_PORT = 5010
#      MESSAGE = "Hello, World!"
      sock = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
      sock.bind((UDP_IP, UDP_PORT))
## ---------- UDP End -----------------



      while(True):
	print 'here'
        img_str, addr = sock.recvfrom(15000) # buffer size is 1024 bytes 
      # CV2
#        print type(img_str)
        nparr = np.fromstring(img_str, np.uint8)
        frame = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
	print type(frame)
        print sys.getsizeof(frame)
        rm = np.reshape(nparr,(60,80,3))
        rrm = cv2.resize(rm,(320,240))
        cv2.imshow('frame',rrm)
##        cv2.imshow('mask',mask)
#    cv2.imshow('res',res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
	   ipCam.close()
           break
