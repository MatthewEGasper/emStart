import logging
import time

from threading import Lock, Thread

from astropy.coordinates import AltAz, EarthLocation, get_moon, get_sun, SkyCoord
from astropy.time import Time
import astropy.units as u

class EarthProcessor():

	_log = logging.getLogger(__name__)

	_config_lock = Lock()
	_station = None
	_target = None
	_is_configured = False

	_az_el_lock = Lock()
	_az = 0
	_el = 0
	
	_ready_lock = Lock()
	_ready = False

	def __init__(self, main):
		self.main = main

		Thread(target = self.configure, daemon = True).start()
		Thread(target = self._run, daemon = True).start()

	def configure(self):
		with self._config_lock:
			self._is_configured = False

		with self._ready_lock:
			self._ready = False

		self._log.info('Collecting ground station information...')
		
		with self._config_lock:
			lat = float(self.main.config.get('station', 'latitude', 0))
			lon = float(self.main.config.get('station', 'longitude', 0))
			ele = float(self.main.config.get('station', 'elevation', 0))

			if abs(lat) > 90:
				self._log.critical('Invalid latitude (' + str(lat) + '°)')
				lat = 0
				self.main.config.set('station', 'latitude', 0)
			if abs(lon) > 180:
				self._log.critical('Invalid longitude (' + str(lon) + '°)')
				lon = 0
				self.main.config.set('station', 'longitude', 0)
			if abs(ele) > 10000:
				self._log.critical('Invalid elevation (' + str(ele) + '°)')
				ele = 0
				self.main.config.set('station', 'elevation', 0)

			self._station = EarthLocation(
				lat = lat * u.deg,
				lon = lon * u.deg,
				height = ele * u.m)

			self._target = self.main.config.get('station', 'target', 'Sun')
			self._log.info('-> Latitude:  ' + str(lat) + '°')
			self._log.info('-> Longitude: ' + str(lon) + '°')
			self._log.info('-> Elevation: ' + str(ele) + 'm')
			self._log.info('-> Target:    \'' + str(self._target) + '\'')

			self._is_configured = True

	def get_az_el(self):
		with self._az_el_lock:
			return self._az, self._el

	def get_target(self):
		with self._config_lock:
			return self._target

	def is_configured(self):
		with self._config_lock:
			return self._is_configured

	def is_ready(self):
		with self._ready_lock:
			return self._ready

	def reset(self):
		self.configure()

	def _get_target(self, ref):
		with self._config_lock:
			target = self._target

		if target.lower() == 'moon':
			target = get_moon(ref)
		elif target.lower() == 'sun':
			target = get_sun(ref)
		else:
			try:
				target = SkyCoord.from_name(target.lower())
			except:
				self._log.critical('Unable to find target \'' + str(target.lower()) + '\'')
				self._is_configured = False
				
				with self._ready_lock:
					self._ready = False
				
				return None

		return target

	def _run(self):
		while True:
			if self.is_configured():
				t = Time(self.main.daemon.get_time())

				target = self._get_target(t)
				if target is not None:
					# get the azimuth and elevation for the target at the specified time and location
					position = target.transform_to(
						AltAz(
							obstime = t,
							location = self._station))

					with self._az_el_lock:
						self._az = position.az.degree
						self._el = position.alt.degree
		
					with self._ready_lock:
						if not self._ready:
							self._ready = True
							self._log.info('Data processor is ready')

			time.sleep(1)

		self._log.critical('Data processor is no longer running')