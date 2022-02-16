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
			self._log.info('ROT2Prog interface closed')

	def set_limits(self):
		"""Sets the hardware limits for azimuth and elevation.
		"""
		if self._rot:
			self._rot.set_limits(
				float(self._main.config.get('limits', 'min_az', -180)),
				float(self._main.config.get('limits', 'max_az', 540)),
				float(self._main.config.get('limits', 'min_el', -21)),
				float(self._main.config.get('limits', 'max_el', 180)))

	def reset(self):
		self.connect()
		self.set_limits()

	def _run(self):
		"""Collects data and sends it to the hardware.
		"""
		while True:
			with self._is_connected_lock:
				if self._is_connected:
					az, el = self._main.processor.get_az_el()
					self._rot.set(az, el)

			time.sleep(1)