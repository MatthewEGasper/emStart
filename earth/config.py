"""Reads and stores information from a configuration file.
"""
import configparser
# import datetime
import logging
import os
# import math
# import time

# from astropy.coordinates import AltAz, EarthLocation, get_sun, get_moon, SkyCoord
# from astropy.time import Time, TimeDelta
# from astropy.timeseries import TimeSeries
# from timezonefinder import TimezoneFinder
# import astropy.units as u
# import numpy as np
# import pytz

class Config():

	"""Summary
	
	Attributes:
	    valid (bool): Description
	"""
	
	valid = False

	_file = ''
	_config = configparser.ConfigParser()

	_log = None
	_log_level = None
	_log_file = None

	_default_log_level = logging.DEBUG
	_default_log_file = 'system.log'

	def __init__(self, file = 'config.ini'):
		"""Summary
		"""
		self._log = logging.getLogger(__name__)

		# select and read the config file
		self._file = file
		self._config.read(self._file)

		# logging setup
		self._log_level = self.get('default', 'log_level', 'int', self._default_log_level)
		self._log_file = self.get('default', 'log_file', 'str', self._default_log_file)
		
		os.makedirs('logs', exist_ok = True)
		logging.basicConfig(filename = 'logs/' + self._log_file, filemode='w', level = self._log_level)
		extra = logging.StreamHandler()
		extra.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
		logging.getLogger().addHandler(extra)

	def get(self, section, key, value_type, default):
		"""Summary
		
		Args:
		    section (TYPE): Description
		    key (TYPE): Description
		    value_type (TYPE): Description
		    default (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		match value_type:
			case 'bool':
				try:
					return self._config.getbool(str(section), str(key))
				except:
					self._log.warning('\'' + str(section) + '\':\'' + str(key) + '\' was not of type \'' + str(value_type) + '\'')
					return bool(default)
			case 'int':
				try:
					return self._config.getint(str(section), str(key))
				except:
					self._log.warning('\'' + str(section) + '\':\'' + str(key) + '\' was not of type \'' + str(value_type) + '\'')
					return int(default)
			case 'float':
				try:
					return self._config.getfloat(str(section), str(key))
				except:
					self._log.warning('\'' + str(section) + '\':\'' + str(key) + '\' was not of type \'' + str(value_type) + '\'')
					return float(default)
			case _:
				try:
					return self._config.get(str(section), str(key))
				except:
					self._log.warning('\'' + str(section) + '\':\'' + str(key) + '\' was not of type \'' + str(value_type) + '\'')
					return str(default)

	def load(self, file = 'config.ini'):
		"""Summary
		
		Args:
		    file (str, optional): Description
		"""
		# select and read the config file
		self._file = file
		self._config.read(self._file)

		# logging setup
		self._log_level = self.get('default', 'log_level', 'int', self._default_log_level)
		self._log_file = self.get('default', 'log_file', 'str', self._default_log_file)

		# display the parsed config file
		self._print_config()
		self.valid = True

	def set(self, section, key, value):
		"""Summary
		
		Args:
		    section (TYPE): Description
		    key (TYPE): Description
		    value (TYPE): Description
		"""
		self._config.set(str(section), str(key), str(value))

	def save(self, file = 'config.ini'):
		"""Summary
		
		Args:
		    file (str, optional): Description
		"""
		try:
			# set all parameters
			self.set('default', 'log_level', self._log_level)
			self.set('default', 'log_file', self._log_file)
			# write to file
			with open(self._file, 'w') as configfile:
				self._config.write(configfile)
		except Exception:
			self._log.warning('Failed to save settings to \'' + str(self._file) + '\'')

	def _print_config(self):
		"""Summary
		"""
		for section in self._config.sections():
			self._log.debug(section + ' : ' + str(dict(self._config[section].items())))

if __name__ == '__main__':
	cfg = Config()
	cfg.load()
	cfg.save()