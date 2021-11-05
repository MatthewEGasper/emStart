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
# Design Name:   simulator.py
# Project Name:  emStart Simulator
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

from parameters import Parameters
from sockets import Sockets
from threading import Lock, Thread
import time
import zmq

class Simulator():

	def __init__(self):
		self.keep_alive = True
		self.time = 0
		self.lock = Lock()
		self.play = False
		self.rewind = False

		# Open communication sockets
		self.params = Parameters()
		self.obsolete = True
		self.sockets = Sockets()
		self.socket = self.sockets.server()

		# Spawn thread to broadcast the time
		Thread(target = self.Timeline, daemon = True).start()
		Thread(target = self.Server, daemon = True).start()

		self.GetCommand()

		return(None)

	def PrintStatus(self):
		print()
		print('Time:   ' + str(self.params.t[self.GetTime()]))
		print('Play:   ' + str(self.play))
		print('Rewind: ' + str(self.rewind))
		print('New:    ' + str(self.obsolete))
		print()

	def GetTime(self):
		with self.lock:
			return(self.time)

	def SetTime(self, t):
		if(t > len(self.params.t)-1):
			t = len(self.params.t)-1
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
					print('Hardware running too slow! Please reduce the speed.')
					self.play = False
				else:
					time.sleep(s)
					# Change the time
					self.SetTime(self.GetTime() + (-1 if self.rewind else 1))

	def GetCommand(self):
		while(self.keep_alive):
			cmd = input('emStart > ')
			try:
				if(cmd in ['play', 'resume', 'continue']):
					self.play = True
				elif(cmd in ['pause', 'break']):
					self.play = False
				elif(cmd in ['rewind', 'replay']):
					self.rewind = not self.rewind
				elif(cmd in ['reset', 'restart']):
					self.play = False
					self.rewind = False
					self.SetTime(0)
				elif(cmd in ['status', 'state']):
					self.PrintStatus()
				elif(cmd in ['config']):
					self.params.Sections()
				elif(cmd.split(' ')[0] in ['load']):
					self.time = 0
					self.play = False
					self.rewind = False
					self.params.Update(section = cmd.split(' ')[1])
					self.obsolete = True
				elif(cmd in ['exit', 'stop', 'quit']):
					self.keep_alive = False
				else:
					raise Exception
			except:
				print('ERROR: Invalid command!')

	def Server(self):
		# Respond to requests with the entire array of data
		while(True):
			request = self.socket.recv_string()
			if('new' in request):
				self.socket.send_json(self.obsolete)
			elif('all' in request):
				self.obsolete = False
				self.socket.send_json([
					self.params.t,
					self.params.alt,
					self.params.az])
			elif('now' in request):
				self.socket.send_json(
					self.params.t[self.GetTime()])
			elif('state' in request):
				t = self.GetTime()
				self.socket.send_json([
					self.params.t[t],
					self.params.alt[t],
					self.params.az[t]])

if __name__ == '__main__':
	Simulator()