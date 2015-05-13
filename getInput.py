#!/usr/bin/env python

import curses
import socket
import time

#initialize UDP Socket
UDP_IP = "192.168.1.212"	#static IP of raspberry pi
#UDP_IP = "127.0.0.1"		#for testing purposes on same computer
UDP_PORT = 5006
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

#intialize curses module
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.halfdelay(1)


lastmessage = "0"

while (True):
 	#clear buffer to prevent overwhelming RasPI with UDP messages when directional keys held down
	curses.flushinp()
	inputKey = stdscr.getch()
	if inputKey == ord('x'): #exit on X key and close curses module
		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()
		curses.endwin()
		break
	#dpad right/left control crane yaw, dpad up/down move rack in and out
	#q rotates claw up, w rotates claw down, a closes claw, s opens claw
	elif inputKey == curses.KEY_RIGHT:
		MESSAGE = "R"
	elif inputKey == curses.KEY_LEFT:
		MESSAGE = "L"
	elif inputKey == curses.KEY_UP:
		MESSAGE = "F"
	elif inputKey == curses.KEY_DOWN:
		MESSAGE = "B"
#	elif inputKey == ord('q'):
#		MESSAGE = "U"
#	elif inputKey == ord('w'):
#		MESSAGE = "D"
	elif inputKey == ord('a'):
		MESSAGE = "C"
	elif inputKey == ord('s'):
		MESSAGE = "O"
	elif inputKey == ord('t'):
		MESSAGE = "T"
	else:
		MESSAGE = "S"
	
	if (lastmessage != MESSAGE):
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

	lastmessage = MESSAGE
	time.sleep(.01)
