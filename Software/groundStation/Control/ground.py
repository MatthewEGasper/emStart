from threading import Lock, Thread
from parameters import Parameters
import serial
import time

class GroundControl():
	
	def __init__(self):
		self.keep_running = True
		self.time = 'Unknown'
		self.lock = Lock()

		self.params = Parameters()

		self.recv_port = '/dev/rfcomm0'
		self.send_port = '/dev/ttyUSB0'

		try:
			self.recv = serial.Serial(port = self.recv_port, baudrate = 9600)
		except:
			print('WARNING: Connection to Earth failed!')

		try:
			self.send = serial.Serial(port = self.send_port, baudrate = 115200)
		except:
			print('WARNING: Connection to antenna failed!')


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
						print('Time: ' + self.time)
				else:
					raise Exception
			except:
				print('ERROR: Invalid command!')

	def Synchronize(self):
		while(True):
			try:
				# Open ground communication
				self.recv.open()
				self.recv.reset_input_buffer()
				# Send request
				self.recv.write(b'!')
				with self.lock:
					# Wait for reply
					char = ''
					self.time = ''
					while(char != '\r'):
						char = self.recv.read(1).decode('utf-8')
						self.time += char
				self.recv.close()
			except:
				self.time = 'Unknown (host not found)'

			time.sleep(0.5)

	def Antenna(self):
		while(True):
			time.sleep(1)
			with self.lock:
				# Send altaz to the Arduino
				self.send.write(self.params.az[self.time].encode('utf-8'))
        self.send.write(b"z")
        self.send.write(self.params.alt[self.time].encode('utf-8'))
        self.send.write(b"n")

if __name__ == '__main__':
	GroundControl()