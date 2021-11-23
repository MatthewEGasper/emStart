from threading import Lock, Thread
from sockets import Sockets
from parameters import Parameters
import time

class GroundControl():
	
	def __init__(self):
		self.keep_running = True
		self.time = 'Unknown'

		params = Parameters()

		# Open communication sockets
		self.sockets = Sockets()
		self.socket = self.sockets.client()
		self.lock = Lock()

		Thread(target=self.Client, daemon = True).start()
		Thread(target=self.Control, daemon = True).start()

		self.GetCommand()
		
		return(None)

	def Client(self):
		while(True):
			with self.lock:
				self.socket.send_string('now')
				self.time = self.socket.recv_json()

	def Control(self):
		while(True):
			with self.lock:
				# Send the data at self.time to the Arduino
				# Data to send is:
				# self.params.alt[self.time]
				# self.params.az[self.time]
				pass

	def GetCommand(self):
		while(self.keep_running):
			cmd = input('ground > ')
			try:
				if(cmd in ['exit', 'stop', 'end', 'quit']):
					self.keep_running = False;
				elif(cmd in ['time']):
					print('Time is: ' + self.time)
			except:
				print('ERROR: Invalid command!')

if __name__ == '__main__':
	GroundControl()