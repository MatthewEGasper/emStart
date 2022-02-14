import logging
import time

from threading import Lock, Thread

from astropy.coordinates import AltAz, EarthLocation, get_moon, get_sun, SkyCoord
from astropy.time import Time
import astropy.units as u

class EarthProcessor():

	_log = logging.getLogger(__name__)

	config_lock = Lock()
	az_el_lock = Lock()

	azimuth = 0
	elevation = 0

	ready = False

	def __init__(self, main):
		self.main = main

		self.configure()
		Thread(target = self._run, daemon = True).start()

	def configure(self):
		self._log.debug('Collecting ground station information...')
		with self.config_lock:
			lat = float(self.main.config.get('station', 'latitude', 0))
			lon = float(self.main.config.get('station', 'longitude', 0))
			height = float(self.main.config.get('station', 'elevation', 0))

			self.station = EarthLocation(
				lat = lat * u.deg,
				lon = lon * u.deg,
				height = height * u.m)

			self.target = self.main.config.get('station', 'target', 'Sun')
			self._log.debug('-> Latitude:  ' + str(lat) + '°')
			self._log.debug('-> Longitude: ' + str(lon) + '°')
			self._log.debug('-> Elevation: ' + str(height) + 'm')
			self._log.debug('-> Target:    \'' + str(self.target) + '\'')

	def get_az_el(self):
		with self.az_el_lock:
			return self.azimuth, self.elevation

	def get_target(self):
		with self.config_lock:
			return self.target

	def _run(self):
		while True:
			with self.config_lock and self.az_el_lock:
				t = Time(self.main.daemon.get_time())

				if self.target.lower() == 'moon':
					target = get_moon(t)
				elif self.target.lower() == 'sun':
					target = get_sun(t)
				else:
					target = SkyCoord.from_name(self.target)

				position = target.transform_to(
					AltAz(
						obstime = t,
						location = self.station))

				if self.azimuth != position.az.degree or self.elevation != position.alt.degree:
					self.azimuth = position.az.degree
					self.elevation = position.alt.degree

					self._log.debug('-> Azimuth: ' + str(round(self.azimuth, 2)) + '°')
					self._log.debug('-> Elevation: ' + str(round(self.elevation, 2)) + '°')

			self.ready = True
			time.sleep(1)