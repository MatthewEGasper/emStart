from datetime import datetime, timezone, timedelta
from threading import Lock, Thread

class EarthDaemon():

	run = True
	runlock = Lock()
	offset = timedelta()
	offsetlock = Lock()

	def __init__(self, config):
		pass
		
	def play(self):
		with self.runlock:
			self.run = True

	def pause(self):
		with self.runlock:
			self.run = False

	def set_offset(self, offset):
		with self.offsetlock:
			self.offset = offset

	def get_time(self):
		return(datetime.now(timezone.utc) + self.offset)

	def override(self):
		pass