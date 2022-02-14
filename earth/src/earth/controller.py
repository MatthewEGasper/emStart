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

	_ser = None
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
				self._ser = ROT2Prog(port = port, timeout = timeout)
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
		try:
			del(self._ser)
		except:
			pass

	def _run(self):
		"""Collects data and sends it to the hardware.
		"""
		while True:
			if self._is_connected:
				with self._is_connected_lock:
					az, el = self._main.processor.get_az_el()
					self._ser.set(az, el)
					refresh_rate = float(self._main.config.get('emulator', 'refresh_rate', 1))
					time.sleep(1 / refresh_rate)