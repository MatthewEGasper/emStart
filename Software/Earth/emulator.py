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
# Engineer:      TJ Scherer
#
# Create Date:   10/1/2021
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
from parameters import Parameters
from threading import Event, Lock, Thread
import time
import zmq

class Emulator():

	def __init__(self):
		self.keep_alive = True
		self.play = False
		self.rewind = False
		self.time = 0
		self.timelock = Lock()

		# Create socket for communication
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.PUB)
		self.socket.bind("tcp://*:5555")

		self.parameters = Parameters()

		# Spawn thread to broadcast the time
		Thread(target = self.Broadcast, daemon = True).start()
		Thread(target = self.Timeline, daemon = True).start()

		return(None)

	def Broadcast(self):
		while(True):
			time.sleep(0.1)
			self.socket.send_json([self.parameters.timearray[self.GetTime()].value, self.parameters.altaz.alt.degree[self.GetTime()], self.parameters.altaz.az.degree[self.GetTime()]])

	def GetTime(self):
		self.timelock.acquire()
		t = self.time
		self.timelock.release()
		return(t)

	# Use a lock for self.time to ensure it is always set within the bounds of the data
	def SetTime(self, t):
		if(t > len(self.parameters.timearray)-1):
			t = len(self.parameters.timearray)-1
			self.play = False

		if(t < 0):
			t = 0
			self.play = False

		self.timelock.acquire()
		self.time = t
		self.timelock.release()

	def Timeline(self):
		starttime = None
		
		while(True):
			if(self.play):
				if(starttime is None):
					starttime = time.time()
				# Sleep
				s = 1/self.parameters.speed - (time.time() - starttime) % 1.0
				if(s < 0):
					print("Emulation running to fast! Reduce the speed and retry.")
					self.play = False
				else:
					time.sleep(s)
					# Move a second
					self.SetTime(self.GetTime() + (-1*self.parameters.interval if self.rewind else self.parameters.interval))
					# print((time.time()-starttime-self.GetTime()))

	def Command(self, cmd):
		try:
			if(cmd in ["play"]):
				self.play = True

			elif(cmd in ["pause"]):
				self.play = False

			elif(cmd in ["rewind"]):
				self.rewind = not self.rewind

			elif(cmd.split(" ")[0] in ["interval"]):
				self.parameters.interval = int(cmd.split(" ")[1])

			elif(cmd.split(" ")[0] in ["set"]):
				self.SetTime(int(cmd.split(" ")[1]))

			elif(cmd.split(" ")[0] in ["move", "skip"]):
				self.SetTime(self.GetTime() + int(cmd.split(" ")[1]))

			elif(cmd in ["exit", "stop", "quit"]):
				self.keep_alive = False

			elif(cmd in ["reload", "refresh"]):
				self.__init__()

			else:
				raise Exception
		except:
			print("ERROR: Invalid command!")

em = Emulator()
time.sleep(2)

# Loop until killed
while(em.keep_alive):
	x = input("em> ")
	em.Command(x)
	time.sleep(1)