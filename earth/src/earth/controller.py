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

	_azimuth = None
	_elevation = None

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
		with self._is_connected_lock:
			try:
				port = self._main.config.get('emulator', 'port', 'COM1')
				timeout = float(self._main.config.get('emulator', 'timeout', 10))
				self._rot = ROT2Prog(port = port, timeout = timeout)
				self._is_connected = True
				self._log.debug('Connected on \'' + port + '\'')
			except:
				self._is_connected = False
				self._log.debug('Failed to connect to \'' + port + '\', please try a different port')

	def disconnect(self):
		"""Removes an existing serial connection.
		"""
		with self._is_connected_lock:
			self._is_connected = False
		if self._rot:
			del(self._rot)

	def set_limits(self):
		"""Sets the hardware limits for azimuth and elevation.
		"""
		if self._rot:
			self._rot.min_az = float(self._main.config.get('limits', 'min_az', 0))
			self._rot.max_az = float(self._main.config.get('limits', 'max_az', 360))
			self._rot.min_el = float(self._main.config.get('limits', 'min_el', 0))
			self._rot.max_el = float(self._main.config.get('limits', 'max_el', 180))

	def _run(self):
		"""Collects data and sends it to the hardware.
		"""
		while True:
			with self._is_connected_lock:
				if self._is_connected:
					az, el = self._main.processor.get_az_el()
					if self._azimuth != az or self._elevation != el:
						self._rot.set(az, el)
					self._azimuth = az
					self._elevation = el

					refresh_rate = float(self._main.config.get('emulator', 'refresh_rate', 1))
					time.sleep(1 / refresh_rate)