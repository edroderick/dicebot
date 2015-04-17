import serial
import numpy as np
import cv2
import time

#open serial communication
port = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1.0)

#set up VideoCapture and frame sizes
cap = cv2.VideoCapture(0)
cap.set(3,160)
cap.set(4,120)

while(True):
	#Capture frame-by-frame
	ret, frame = cap.read()
	#Display the resulting frame
	#Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	#define range of blue color in HSV
#	lower_blue = np.array([110, 50, 50], dtype=np.uint8)
#	upper_blue = np.array([130,255,255], dtype=np.uint8)
#	lower_cyan = np.array([ 95, 50, 50], dtype=np.uint8)
#	upper_cyan = np.array([110,255,255], dtype=np.uint8)
	lower_red = np.array([ 0,100,100], dtype=np.uint8)
	upper_red = np.array([30,255,255], dtype=np.uint8)
	
	#Threshold the HSV image to get only blue colors
#	mask = cv2.inRange(hsv, lower_blue, lower_blue)
#	mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
	mask = cv2.inRange(hsv, lower_red, upper_red)
	
	#contours setup and send moments for the OpenCM
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	
	max_area = 0
	largest_contour = None
	for idx, contour in enumerate(contours):
	    area = cv2.contourArea(contour)
	    if area > max_area:
		max_area = area
		largest_contour = contour
	if not largest_contour == None:
	    M = cv2.moments(mask)
	   
	    if M['m00']!= 0:
		if area == 0:
		   area = 1
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
#		print cx
		pcx = (((cx*0.00625)*2.0)-1.0)
#		print type(pcx)
		fov = 60
		theta = (fov*2.0)*pcx
		thetad = 0
		etheta = thetad - theta
#		print etheta
		
		kp = 0.1
		kd = 1
		ki = 1
		PID = kd*ki*kp*etheta
#		print "PID: "+ str(PID)
		
		a = int(0)
#		print "a = int(0): "+ str(a)
		a = a|(int(np.abs(PID)) & 0x7F)
#		print a
#		print ("a: "+str(a))
		if (PID < 0):
	 	    a = a|0X80
#		print a
		stra = str(a)
#		print stra + " : " + bin(a)
		port.write(stra + '\r')


		#draw the box around the moments
		rect = cv2.minAreaRect(largest_contour)
		rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
#		print largest_contour
#		print "rect 0,0: ",  rect[0][0]
#		print "rect 0,1: ",  rect[0][1]
		print max_area
		print max_area/(120.0*160.0)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(frame, [box], 0, (255,0,0), 2)
	#Bitwise-And mask and original image
#	res = cv2.bitwise_and(frame,frame,mask = mask)
	
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
#	port.write(strpcx)
#	cv2.imshow('res', res)

	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break	
