import logging

from datetime import datetime, timezone, timedelta
from threading import Lock, Thread

class EarthDaemon():

	_log = logging.getLogger(__name__)

	is_playing_lock = Lock()
	is_playing = False

	time_lock = Lock()
	time = datetime.now(timezone.utc)
	
	start_time_lock = Lock()
	start_time = datetime.now(timezone.utc)

	played_at = datetime.now(timezone.utc)

	def __init__(self, config):
		Thread(target = self.run, daemon = True).start()

	def play(self):
		with self.is_playing_lock:
			self.is_playing = True
			self._log.info('Playing')

			self.played_at = datetime.now(timezone.utc)

	def pause(self):
		with self.is_playing_lock:
			self.is_playing = False
			self._log.info('Paused')

			with self.start_time_lock:
				self.start_time += datetime.now(timezone.utc) - self.played_at

	def get_time(self):
		with self.time_lock:
			return self.time

	def set_time(self, time = None):
		with self.time_lock and self.start_time_lock:
			if time == None:
				self.time = self.start_time = datetime.now(timezone.utc)
			else:
				self.time = self.start_time = time

	def run(self):
		while True:
			with self.is_playing_lock:
				if self.is_playing:
					with self.time_lock and self.start_time_lock:
						self.time = self.start_time + (datetime.now(timezone.utc) - self.played_at)