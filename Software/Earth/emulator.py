################################################################
#
# ███████╗███╗   ███╗███████╗████████╗ █████╗ ██████╗ ████████╗
# ██╔════╝████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
# █████╗  ██╔████╔██║███████╗   ██║   ███████║██████╔╝   ██║   
# ██╔══╝  ██║╚██╔╝██║╚════██║   ██║   ██╔══██║██╔══██╗   ██║   
# ███████╗██║ ╚═╝ ██║███████║   ██║   ██║  ██║██║  ██║   ██║   
# ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  
#
################################################################
# School:        Embry-Riddle Daytona Beach
# Engineers:     Ivan Borra and TJ Scherer
#
# Create Date:   11/8/2021
# Design Name:   emulator.py
# Project Name:  emStart Emulator
# Tool Versions: Python 3.9.7
# Description:   
#
# Dependencies:  
#
# Revision:      0.0
# Revision 0.0 - File Created
#
# Additional Comments: 
#
################################################################

from datetime import datetime
from math import cos, radians, sin
from pymycobot import MyCobot, utils
from sockets import Sockets
import serial.tools.list_ports
import time

class Emulator():

	def __init__(self):
		# Open communication sockets
		self.sockets = Sockets()
		self.socket = self.sockets.client()

		self.port = self.GetPort()
		
		if(self.port is not None):
			self.mycobot = MyCobot(self.port, 115200, debug = True)

		self.MoveArm(0, 0)

		self.Run()

		return(None)

	def GetPort(self):
		# Determine the serial port
		port = utils.detect_port_of_basic()
		if port is not None:
			return(port)

		ports = serial.tools.list_ports.comports()

		# No ports found
		if(not ports):
			print('WARNING: No ports found!')
			return(None)

		# Display all ports
		for port, desc, hwid in sorted(ports):
			print("{}: {} [{}]".format(port, desc, hwid))

		# Process user input
		while(1):
			x = input('Device Port: ')
			if(x in ['debug', 'none', 'None']):
				print('INFO: Running in debug.')
				return(None)
			for port, desc, hwid in sorted(ports):
				if(x in [port, desc, hwid]):
					return(x)

	def Run(self):
		starttime = None
		last_alt = 0
		last_az = 0

		while(True):
			if(starttime is None):
				starttime = time.time()

			self.socket.send_string('position')
			self.alt, self.az = self.socket.recv_json()

			# Convert values
			if(self.alt < -90 or self.alt > 90):
				print('WARNING: Altitude angle ' + str(round(self.alt, 2)) + ' out of bounds.')
				self.alt = 0

			while(self.az > 180):
				self.az -= 360	
			while(self.az < -180):
				self.az += 360
			if(self.az < -175 or self.az > 175):
				print('WARNING: Azimuth angle ' + str(round(self.az, 2)) + ' out of bounds.')
				self.az = 0

			if(self.alt != last_alt or self.az != last_az):
				self.MoveArm(self.alt, self.az)
				print(str(datetime.now()) + ':\t' + str(round(self.alt, 2)) + ',\t' + str(round(self.az, 2)))

			last_alt = self.alt
			last_az = self.az
			
			# Sleep
			time.sleep(1.0 - (time.time() - starttime) % 1.0)

	def MoveArm(self, J5, J6):
		# J1: -165 to 165
		# J2: -165 to 165
		# J3: -165 to 165
		# J4: -165 to 165
		# J5: -165 to 165
		# J6: -175 to 175
		if(self.port is not None):
			self.mycobot.sync_send_angles([0, 0, 0, 0, J5, J6], 100)

if __name__ == '__main__':
	Emulator()

# mc=MyCobot(PI_PORT, PI_BAUD) ## connects to the arm from Raspberry Pi

# def getdata(): # function made to gather coordinate and angle data.
# 	coords = mc.get_coords() # get_coords() records the coordinate data of all joints.
# 	print("\nCoords:")
# 	print(coords) # prints out coordinate data
# 	angle_datas = mc.get_angles()  # get_angles() records the angle position of all joints
# 	print("\nAngle:")
# 	print(angle_datas)  # prints out joint location


# print("\nstartup data:\n")
# getdata()
# ##
# mc.send_angles([0, 0, 0, 0, 0, 0], 50)  #sends all joints to default position at 50% speed
# print(mc.is_paused())
# time.sleep(2.5) # delay added to allow time for the robot to move into place before recording data
# print("\nstartup data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J2.value, 90, 50) # sets joint 2 to 90 degrees
# time.sleep(2.5)
# mc.pause() # pauses arm movement code to allow for brief delay between next command.
# time.sleep(2.5)
# print("\njoint 2 data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J1.value, 90, 50) # sets joint 1 to 90 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 90 degrees data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J1.value, 180, 50) # sets joint 1 to 180 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 180 degrees data:\n")
# getdata()
# time.sleep(1)
# ##
# mc.send_angles(Angle.J1.value, -90, 50) # sets joint 1 to 270=-90 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 -90 degrees data:\n")
# getdata()
# time.sleep(1)
# ##
# mc.send_angles(Angle.J1.value, 0, 50) # sets joint 1 to 0 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 0 degrees data:\n")
# getdata()
# time.sleep(1)

# By taking the robot arm at its full length  (280 mm) joint 1 can be the core of the earth and the other arms rotate around it.
# by moving the robot arm around in a full circle and getting the data of angles and coordinates we can create our own latitude and longitude cordintate system.
