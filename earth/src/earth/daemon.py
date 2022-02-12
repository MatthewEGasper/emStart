"""Maintains the time of the test.
"""
import logging
from datetime import datetime, timezone, timedelta
from threading import Lock, Thread

class EarthDaemon():

	"""Spawns a thread which updates the test time in real time.
	"""
	
	_log = logging.getLogger(__name__)

	_is_playing_lock = Lock()
	_is_playing = False

	_time_lock = Lock()
	_time = datetime.now(timezone.utc)
	
	_start_time_lock = Lock()
	_start_time = datetime.now(timezone.utc)

	_played_at = datetime.now(timezone.utc)

	def __init__(self):
		"""Creates object and starts the time thread
		"""
		Thread(target = self._run, daemon = True).start()

	def play(self):
		"""Allows test time to pass.
		"""
		with self._is_playing_lock:
			self._is_playing = True
			self._played_at = datetime.now(timezone.utc)
			self._log.debug('Playing from ' + str(self.get_time()))

	def pause(self):
		"""Pauses the test.
		"""
		with self._is_playing_lock:
			self._is_playing = False
			with self._start_time_lock:
				self._start_time += datetime.now(timezone.utc) - self._played_at
			self._log.debug('Paused at    ' + str(self.get_time()))

	def get_time(self):
		"""Summary
		
		Returns:
		    datetime: The current UTC datetime of the test.
		"""
		with self._time_lock:
			return self._time

	def set_time(self, time = None):
		"""Summary
		
		Args:
		    time (datetime, optional): Set the UTC datetime of the test. When unspecified, use the current system date and time.
		"""
		with self._time_lock and self._start_time_lock:
			if time == None:
				self._time = self._start_time = datetime.now(timezone.utc)
			else:
				self._time = self._start_time = time

	def _run(self):
		"""Update the current time based on the state of the test.
		"""
		while True:
			with self._is_playing_lock:
				if self._is_playing:
					with self._time_lock and self._start_time_lock:
						self._time = self._start_time + (datetime.now(timezone.utc) - self._played_at)