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

	_time_multiplier = 1

	def __init__(self):
		"""Creates object and starts the time thread.
		"""
		Thread(target = self._run, daemon = True).start()

	def is_playing(self):
		"""Indicates if the test is running.
		
		Returns:
		    bool: Whether or not the test is running.
		"""
		with self._is_playing_lock:
			return self._is_playing

	def play(self):
		"""Allows test time to pass.
		"""
		with self._is_playing_lock:
			if not self._is_playing:
				self._played_at = datetime.now(timezone.utc)
				self._is_playing = True
				self._log.info('Playing from ' + str(self.get_time()))

	def pause(self):
		"""Pauses the test.
		"""
		with self._is_playing_lock:
			if self._is_playing:
				with self._start_time_lock:
					self._start_time += self._time_multiplier * (datetime.now(timezone.utc) - self._played_at)
					self._is_playing = False
					self._log.info('Paused at ' + str(self.get_time()))

	def sync(self):
		self.set_speed()
		self.play()
		self.set_time()

	def get_time(self):
		"""Returns the current test time.
		
		Returns:
		    datetime: The current UTC datetime of the test.
		"""
		with self._time_lock:
			return self._time

	def set_time(self, time = None):
		"""Sets the test time.
		
		Args:
		    time (datetime, optional): Set the UTC datetime of the test. When unspecified, use the current system date and time.
		"""
		with self._time_lock and self._start_time_lock:
			if time == None:
				self._time = self._start_time = datetime.now(timezone.utc)
			else:
				self._time = self._start_time = datetime.fromisoformat(time)
		self._log.info('Time set to ' + str(self._time))

	def get_speed(self):
		"""Returns the time scale for the test.
		
		Returns:
		    int: Time multiplier, higher values pass time faster, lower values pass time slower.
		"""
		return self._time_multiplier

	def set_speed(self, speed = 1):
		"""Set the time scale for the test.
		
		Args:
		    speed (int): Time multiplier, higher values pass time faster, lower values pass time slower.
		"""
		if self._is_playing:
			replay = True
		else:
			replay = False

		self.pause()
		self._time_multiplier = int(speed)
		
		if replay:
			self.play()

	def reset(self):
		self.pause()
		self.set_time()
		self.set_speed()

	def _run(self):
		"""Update the current time based on the state of the test.
		"""
		while True:
			with self._is_playing_lock:
				if self._is_playing:
					with self._time_lock and self._start_time_lock:
						self._time = self._start_time + (self._time_multiplier * (datetime.now(timezone.utc) - self._played_at))