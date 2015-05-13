import socket
import time
import serial

UDP_IP_IN = "<your RPIs IP address here>"
#UDP_IP_OUT = "<your RPIs IP address here>"
UDP_PORT_IN = 5006
#UDP_PORT_OUT = 5006

ser = serial.Serial('/dev/ttyAMA0', 9600)	#RPI hardware serial
#ser = serial.Serial('/dev/ttyACM0', 38400)	#USB

sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP from Control CPU
sock_in.bind((UDP_IP_IN, UDP_PORT_IN))

#leaving 1 bit space to add direction in future
maxspeed = 127 #0b1111111
stepsize = 10 #angle of step for claw

while True:
	data, addr = sock_in.recvfrom(1024) # buffer size is 1024 bytes
	msg = 0

	if (data[0] == "F"):
		msg = chr(70)
		value = chr(255)
	elif (data[0] == "B"):
		msg = chr(66)
		value = chr(255)
	elif (data[0] == "L"):
		msg = chr(76)
		value = chr(255)
	elif (data[0] == "R"):
		msg = chr(82)
		value = chr(255)
	elif (data[0] == "O"):
		msg = chr(79)
		value = chr(255)
	elif (data[0] == "C"):
		msg = chr(67)
		value = chr(255)
	elif (data[0] == "T"):
		msg = chr(84)
		value = chr(255)
	elif (data[0] == "S"):
		msg = chr(83)
		value = chr(255)
	
	if (msg != 0):
		packet = msg + value
		print packet
		ser.write(packet)

	time.sleep(.01)
