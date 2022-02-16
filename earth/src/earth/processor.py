import logging
import time

from threading import Lock, Thread

from astropy.coordinates import AltAz, EarthLocation, get_moon, get_sun, SkyCoord
from astropy.time import Time
import astropy.units as u

class EarthProcessor():

	_log = logging.getLogger(__name__)

	_config_lock = Lock()
	_az_el_lock = Lock()
	_ready_lock = Lock()

	_is_configured_lock = Lock()
	_is_configured = False

	_station = None
	_target = None
	_azimuth = 0
	_elevation = 0

	_ready = False

	def __init__(self, main):
		self.main = main

		self.configure()
		Thread(target = self._run, daemon = True).start()

	def configure(self):
		self._log.info('Collecting ground station information...')
		with self._config_lock:
			lat = float(self.main.config.get('station', 'latitude', 0))
			lon = float(self.main.config.get('station', 'longitude', 0))
			height = float(self.main.config.get('station', 'elevation', 0))

			self._station = EarthLocation(
				lat = lat * u.deg,
				lon = lon * u.deg,
				height = height * u.m)

			self._target = self.main.config.get('station', 'target', 'Sun')
			self._log.info('-> Latitude:  ' + str(lat) + '°')
			self._log.info('-> Longitude: ' + str(lon) + '°')
			self._log.info('-> Elevation: ' + str(height) + 'm')
			self._log.info('-> Target:    \'' + str(self._target) + '\'')

		with self._is_configured_lock:
			self._is_configured = True

	def get_az_el(self):
		with self._az_el_lock:
			return self._azimuth, self._elevation

	def get_target(self):
		with self._config_lock:
			return self._target

	def is_ready(self):
		with self._ready_lock:
			return self._ready

	def reset(self):
		with self._ready_lock:
			self._ready = False
		with self._is_configured_lock:
			self._is_configured = False
		self.configure()

	def _run(self):
		while True:
			with self._is_configured_lock:
				if self._is_configured:
					with self._config_lock and self._az_el_lock:
						t = Time(self.main.daemon.get_time())

						if self._target.lower() == 'moon':
							target = get_moon(t)
						elif self._target.lower() == 'sun':
							target = get_sun(t)
						else:
							target = SkyCoord.from_name(self._target)

						# get the azimuth and elevation for the target at the specified time and location
						position = target.transform_to(
							AltAz(
								obstime = t,
								location = self._station))

						if self._azimuth != position.az.degree or self._elevation != position.alt.degree:
							self._azimuth = position.az.degree
							self._elevation = position.alt.degree

							self._log.debug('-> Azimuth: ' + str(round(self._azimuth, 2)) + '°')
							self._log.debug('-> Elevation: ' + str(round(self._elevation, 2)) + '°')
			
					with self._ready_lock:
						if not self._ready:
							self._ready = True
							self._log.info('Data processor is ready')

			time.sleep(1)