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

	_az_el_lock = Lock()
	_azimuth = 0
	_elevation = 0

	_target_az_el_lock = Lock()
	_target_azimuth = 0
	_target_elevation = 0
	
	_ready_lock = Lock()
	_ready = False

	_is_configured_lock = Lock()
	_is_configured = False

	def __init__(self, main):
		self.main = main

		Thread(target = self.configure, daemon = True).start()
		Thread(target = self._run, daemon = True).start()

	def configure(self):
		with self._is_configured_lock:
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

		with self._is_configured_lock:
			self._is_configured = True

	def get_az_el(self):
		with self._az_el_lock:
			return self._azimuth, self._elevation

	def get_target(self):
		with self._config_lock:
			return self._target

	def get_target_az_el(self):
		with self._target_az_el_lock:
			return self._target_azimuth, self._target_elevation

	def is_ready(self):
		with self._ready_lock:
			return self._ready

	def reset(self):
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
							try:
								target = SkyCoord.from_name(self._target.lower())
							except:
								self._log.critical('Unable to find target \'' + str(self._target.lower()) + '\'')
								self._is_configured = False
								with self._ready_lock:
									self._ready = False
								return

						# get the azimuth and elevation for the target at the specified time and location
						position = target.transform_to(
							AltAz(
								obstime = t,
								location = self._station))

						az = position.az.degree
						el = position.alt.degree

						# the Earth azimuth should be a 180° offset from the target azimuth
						self._target_azimuth = az
						if az < 180:
							self._azimuth = az + 180
						else:
							self._azimuth = az - 180

						# both share the same elevation angle
						self._target_elevation = self._elevation = el
			
					with self._ready_lock:
						if not self._ready:
							self._ready = True
							self._log.info('Data processor is ready')

			time.sleep(1)