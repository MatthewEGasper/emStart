from threading import Lock, Thread
from parameters import Parameters
import serial
import time

class GroundControl():
	
	def __init__(self):
		self.keep_running = True
		self.time = 'Uninitialized'
		self.lock = Lock()
		self.recv_port = '/dev/rfcomm0'
		self.send_port = '/dev/???'

		params = Parameters()

		Thread(target=self.Synchronize, daemon = True).start()
		Thread(target=self.Antenna, daemon = True).start()

		self.GetCommand()
		
		return(None)

	def GetCommand(self):
		while(self.keep_running):
			cmd = input('ground > ')
			try:
				if(cmd in ['exit', 'stop', 'end', 'quit']):
					self.keep_running = False;
				elif(cmd in ['time']):
					with self.lock:
						print('INFO: ' + self.time)
				else:
					raise Exception
			except:
				print('ERROR: Invalid command!')

	def Synchronize(self):
		while(True):
			try:
				# Open ground communication
				recv = serial.Serial(port = self.recv_port, baudrate = 9600)
				recv.reset_input_buffer()
				# Send request
				recv.write(b'!')
				with self.lock:
					# Wait for reply
					char = ''
					self.time = ''
					while(char != '\r'):
						char = recv.read(1).decode('utf-8')
						self.time += char
				recv.close()
			except:
				self.time = 'Unable to establish connection to Earth!'
				pass

			time.sleep(0.5)

	def Antenna(self):
		while(True):
			time.sleep(1)
			with self.lock:
				# Send altaz to the Arduino
				pass

if __name__ == '__main__':
	GroundControl()