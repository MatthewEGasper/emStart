import logging

from datetime import datetime, timezone, timedelta
from threading import Lock, Thread

class EarthDaemon():

	_log = logging.getLogger(__name__)

	_is_playing_lock = Lock()
	_is_playing = False

	_time_lock = Lock()
	_time = datetime.now(timezone.utc)
	
	_start_time_lock = Lock()
	_start_time = datetime.now(timezone.utc)

	_played_at = datetime.now(timezone.utc)

	def __init__(self, config):
		Thread(target = self._run, daemon = True).start()

	def play(self):
		with self._is_playing_lock:
			self._is_playing = True
			self._played_at = datetime.now(timezone.utc)
			self._log.debug('Playing from ' + str(self.get_time()))

	def pause(self):
		with self._is_playing_lock:
			self._is_playing = False
			with self._start_time_lock:
				self._start_time += datetime.now(timezone.utc) - self._played_at
			self._log.debug('Paused at    ' + str(self.get_time()))

	def get_time(self):
		with self._time_lock:
			return self._time

	def set_time(self, time = None):
		with self._time_lock and self._start_time_lock:
			if time == None:
				self._time = self._start_time = datetime.now(timezone.utc)
			else:
				self._time = self._start_time = time

	def _run(self):
		while True:
			with self._is_playing_lock:
				if self._is_playing:
					with self._time_lock and self._start_time_lock:
						self._time = self._start_time + (datetime.now(timezone.utc) - self._played_at)