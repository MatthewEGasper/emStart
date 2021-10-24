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
from sockets import Sockets
from threading import Event, Lock, Thread
import time
import zmq

class Emulator():

	def __init__(self):
		self.keep_alive = True
		self.play = False
		self.rewind = False
		self.time = 0
		self.lock = Lock()
		self.loading = True

		self.params = Parameters()
		self.sockets = Sockets()
		self.pub_time = self.sockets.pub_time()
		self.rep_data = self.sockets.rep_data()

		# Spawn thread to broadcast the time
		Thread(target = self.publish_time, daemon = True).start()
		Thread(target = self.reply_data, daemon = True).start()
		Thread(target = self.Timeline, daemon = True).start()

		return(None)

	def GetTime(self):
		with self.lock:
			return(self.time)

	# Use a lock for self.time to ensure it is always set within the bounds of the data
	def SetTime(self, t):
		if(t > len(self.params.timearray)-1):
			t = len(self.params.timearray)-1
			self.play = False

		if(t < 0):
			t = 0
			self.play = False

		with self.lock:
			self.time = t

	def Timeline(self):
		starttime = None
		while(True):
			if(self.play):
				if(starttime is None):
					starttime = time.time()
				# Sleep
				s = 1/self.params.speed - (time.time() - starttime) % 1.0
				if(s < 0):
					print("Emulation running to fast! Reduce the speed and retry.")
					self.play = False
				else:
					time.sleep(s)
					# Move a second
					self.SetTime(self.GetTime() + (-1*self.params.interval if self.rewind else self.params.interval))
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
				self.params.interval = int(cmd.split(" ")[1])

			elif(cmd.split(" ")[0] in ["set"]):
				self.SetTime(int(cmd.split(" ")[1]))

			elif(cmd.split(" ")[0] in ["move", "skip"]):
				self.SetTime(self.GetTime() + int(cmd.split(" ")[1]))

			elif(cmd in ["exit", "stop", "quit"]):
				self.keep_alive = False

			else:
				raise Exception
		except:
			print("ERROR: Invalid command!")

	def publish_time(self):
		# Continuously broadcast the current time, altitude, and azimuth
		while(True):
			time.sleep(0.1)
			data = [
				self.params.timearray[self.GetTime()].value,
				self.params.altaz.alt.degree[self.GetTime()],
				self.params.altaz.az.degree[self.GetTime()]]
			self.pub_time.send_json(data)

	def reply_data(self):
		# Respond to requests with the entire array of data
		while(True):
			self.rep_data.recv()
			data = [
				[str(i) for i in self.params.timearray],
				self.params.altaz.alt.degree.tolist(),
				self.params.altaz.az.degree.tolist()]
			self.rep_data.send_json(data)
			self.loading = False

em = Emulator()
while(em.loading):
	pass
time.sleep(1)

# Loop until killed
while(em.keep_alive):
	x = input("em> ")
	em.Command(x)
	time.sleep(1)