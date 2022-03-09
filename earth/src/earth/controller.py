"""Send serial commands to ROT2Prog.
"""
import logging
import time

from rot2prog import ROT2Prog
from threading import Lock, Thread

class EarthController():

	"""Reads current position from daemon and sends it to hardware.
	"""
	
	_log = logging.getLogger(__name__)

	_rot = None
	_is_connected = False
	_is_connected_lock = Lock()

	def __init__(self, main):
		"""Creates object and attempts to establish connection.
		
		Args:
		    main (Earth): Top level object used for function calls.
		"""
		self._main = main
		Thread(target = self.connect, daemon = True).start()
		Thread(target = self._run, daemon = True).start()
		
	def connect(self):
		"""Attempts to establish serial connection.
		"""
		self.disconnect()
		self.set_limits()
		with self._is_connected_lock:
			port = self._main.config.get('emulator', 'port', 'COM1')
			timeout = float(self._main.config.get('emulator', 'timeout', 10))
			try:
				self._rot = ROT2Prog(port = port, timeout = timeout)
				self._is_connected = True
				self._log.info('ROT2Prog connected on \'' + port + '\'')
			except:
				self._is_connected = False
				self._log.info('ROT2Prog failed to connect on \'' + port + '\'')

	def disconnect(self):
		"""Removes an existing serial connection.
		"""
		with self._is_connected_lock:
			self._is_connected = False
		if self._rot:
			del(self._rot)
			self._log.info('ROT2Prog disconnected')

	def is_connected(self):
		with self._is_connected_lock:
			return self._is_connected

	def get_az_el(self):
		with self._is_connected_lock:
			if self._is_connected:
				try:
					return self._rot.status()
				except:
					self.disconnect()
					return (0, 0)

	def set_limits(self):
		"""Sets the hardware limits for azimuth and elevation.
		"""
		if self.is_connected():
			self._rot.set_limits(
				float(self._main.config.get('limits', 'min_az', -180)),
				float(self._main.config.get('limits', 'max_az', 540)),
				float(self._main.config.get('limits', 'min_el', -21)),
				float(self._main.config.get('limits', 'max_el', 180)))
		else:
			self._log.warning('Unable to set limits when controller is disconnected')

	def reset(self):
		self.connect()

	def _run(self):
		"""Collects data and sends it to the hardware.
		"""
		while True:
			with self._is_connected_lock:
				if self._is_connected:
					az, el = self._main.processor.get_az_el()
					
					try:
						self._rot.set(az, el)
					except Exception as e:
						self._log.critical('Failed to send to controller (' + str(e) + ')')

					try:
						self._rot.status()
					except:
						self.disconnect()

			time.sleep(1)