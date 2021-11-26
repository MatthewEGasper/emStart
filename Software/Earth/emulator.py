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
from pymycobot import MyCobot, utils
from sockets import Sockets
import serial.tools.list_ports
import time

class Emulator():

	def __init__(self):
		# Open data communication sockets
		self.sockets = Sockets()
		self.socket = self.sockets.client()

		# Open arm command port
		self.port = self.GetPort()
		
		if(self.port is not None):
			self.mycobot = MyCobot(self.port, 115200)
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
			x = input('Select device port: ')
			if(x in ['debug']):
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

			if(self.alt != last_alt or self.az != last_az):
				self.MoveArm(self.alt, self.az)
				print('INFO: ' + str(datetime.now()) + ':\t' + str(round(self.alt, 2)) + ',\t' + str(round(self.az, 2)))

			last_alt = self.alt
			last_az = self.az
			
			# Sleep
			time.sleep(1 - (time.time() - starttime) % 1)

	def MoveArm(self, J5, J6):
		if(self.port is not None):
			# Convert values
			J5 *= -1
			J5 -= 90
			while(J5 > 0):
				J5 -= 90
			while(J5 < -180):
				J5 += 90

			while(J6 > 180):
				J6 -= 360	
			while(J6 < -180):
				J6 += 360

			if(J6 < -175):
				J6 = -175
			if(J6 > 175):
				J6 = 175

			self.mycobot.sync_send_angles([J5/2, 0, 0, 0, J5/2, J6], 50)

if __name__ == '__main__':
	Emulator()