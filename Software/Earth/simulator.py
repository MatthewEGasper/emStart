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
		self.time_lock = Lock()
		self.server_lock = Lock()
		self.play = False
		self.rewind = False

		self.params = Parameters()
		
		# Open communication sockets
		self.obsolete = True
		self.sockets = Sockets()
		self.socket = self.sockets.server()

		# Spawn thread to manage the simulation time
		Thread(target = self.Timeline, daemon = True).start()
		# Spawn thread to respond to client requests
		Thread(target = self.Server, daemon = True).start()
		# Wait for user requests
		self.GetCommand()

		return(None)

	def PrintStatus(self):
		# Print the current state of the simulation
		print()
		print('Config: ' + str(self.params.section))
		print('Play:   ' + str(self.play))
		print('Rewind: ' + str(self.rewind))
		print('New:    ' + str(self.obsolete))
		print()
		with self.server_lock:
			print('Sample: ' + str(self.GetTime()) + ' of ' + str(len(self.params.t)-1))
		print('Time:   ' + str(self.params.t[self.GetTime()]))
		print('Alt:    ' + str(round(self.params.alt[self.GetTime()], 2)))
		print('Az:     ' + str(round(self.params.az[self.GetTime()], 2)))
		print()

	def GetTime(self):
		# Get the simulation time
		with self.time_lock:
			return(self.time)

	def SetTime(self, t):
		# Set the simulation time
		if(t > len(self.params.t)-1):
			t = len(self.params.t)-1
			self.play = False

		if(t < 0):
			t = 0
			self.play = False

		with self.time_lock:
			self.time = t

	def Timeline(self):
		# Manage the current simulation time
		starttime = None
		while(True):
			if(self.play):
				if(starttime is None):
					starttime = time.time()
				# Sleep
				s = self.params.slowness - (time.time() - starttime) % 1.0
				if(s < 0):
					print('Hardware running too slow! Please reduce the speed and try again.')
					self.play = False
				else:
					time.sleep(s)
					# Change the time
					self.SetTime(self.GetTime() + (-1 if self.rewind else 1))

	def GetCommand(self):
		# Respond to user requests
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
					time.sleep(1)
					self.SetTime(0)
				elif(cmd in ['status', 'state']):
					self.PrintStatus()
				elif(cmd in ['config', 'list', 'sections', 'saves']):
					self.params.Sections()
				elif(cmd.split(' ')[0] in ['load']):
					self.play = False
					self.rewind = False
					time.sleep(1)
					self.SetTime(0)
					with self.server_lock:
						self.params.Update(section = cmd.split(' ')[1])
					self.obsolete = True
					print('INFO: Please refresh the user interface if it has not updated.')
				elif(cmd in ['exit', 'stop', 'quit']):
					self.keep_alive = False
				else:
					raise Exception
			except:
				print('ERROR: Invalid command!')

	def Server(self):
		# Respond to client requests
		while(True):
			request = self.socket.recv_string()
			if('new' in request):
				self.socket.send_json(self.obsolete)
			elif('all' in request):
				self.obsolete = False
				with self.server_lock:
					self.socket.send_json([
						self.params.t,
						self.params.alt,
						self.params.az])
			elif('now' in request):
				t = self.params.t[self.GetTime()]
				with self.server_lock:
					self.socket.send_json(t)
			elif('position' in request):
				t = self.GetTime()
				with self.server_lock:
					self.socket.send_json([
						self.params.alt[t],
						self.params.az[t]])

if __name__ == '__main__':
	Simulator()