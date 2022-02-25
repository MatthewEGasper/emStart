"""Exchanges information with a configuration file.
"""
import configparser
import logging
import os

class EarthConfig():

	"""Reads configuration from a file into a modifiable dictionary, which can be saved.
	"""
	
	_config_file = None
	_config = configparser.ConfigParser()

	_root_log = logging.getLogger()
	_root_log_level = None
	_root_log_file = None

	_default_root_log_level = logging.DEBUG
	_default_root_log_file = '/logs/system.log'

	_log = logging.getLogger(__name__)

	def __init__(self, file):
		"""Creates object and initializes the root logger.
		
		Args:
		    file (str): Name of the configuration file.
		"""
		# select and read the config file
		self._config_file = file
		self._config.read(self._config_file)

		# quiet is set to true because logging is not set up yet, so it cannot log any info messages
		self._root_log_level = int(self.get('logging', 'level', self._default_root_log_level, quiet = True))
		self._root_log_file = self.get('logging', 'file', self._default_root_log_file, quiet = True)

		# set the base root log level to record everything
		self._root_log.setLevel(0)

		# set the root log file
		try:
			os.makedirs(os.path.dirname('../' + self._root_log_file), exist_ok = True)
			self._log.debug("Created directory " + str(os.path.dirname(self._root_log_file)))
		except FileExistsError:
			pass # if the file already exists, there is no need to create it or handle the error

		# set the root log format
		formatter = logging.Formatter('%(levelname)-10s %(name)-20s %(message)s')

		# create handler for stream io
		_stream_handler = logging.StreamHandler()
		_stream_handler.setLevel(self._root_log_level) # filter out log messages based on use configuration
		_stream_handler.setFormatter(formatter)
		self._root_log.addHandler(_stream_handler)
		
		# create handler for file io to record everything
		_file_handler = logging.FileHandler('../' + self._root_log_file, mode = 'w')
		_stream_handler.setLevel(self._root_log_level) # filter out log messages based on use configuration
		_file_handler.setFormatter(formatter)
		self._root_log.addHandler(_file_handler)

		self._log.info('Log level: ' + str(self._root_log_level))
		self._log.info('Log file: ' + str(self._root_log_file))
		self._print_config()

	def get(self, section, key, default = 'Unknown', quiet = False):
		"""Determines the value of a given key whether it exists or not.
		
		Args:
		    section (str): Name of the section to search for the requested value.
		    key (str): Name of key paired to the requested value.
		    default (str): Value to return if the requested value is invalid.
		    quiet (bool, optional): When true, disables logging. This is required for calls made prior to initialization of the logger.
		
		Returns:
		    str: Value paired to the given key.
		"""
		try:
			return self._config.get(str(section), str(key))
		except:
			if not quiet:
				self._log.warning('Could not determine value of \'' + str(section) + '\':\'' + str(key) + '\', returning \'' + str(default) + '\' instead')
			self.set(str(section), str(key), default)
			return default

	def open(self, file = None):
		"""Opens a configuration file.
		
		Args:
		    file (str, optional): Name of the configuration file. Leaving this blank will use the current file.
		"""
		if file is not None:
			self._config_file = file
			self._log.info('Loading \'' + str(self._config_file) + '\'')
		else:
			self._log.info('Reloading \'' + str(self._config_file) + '\'')
		
		self._config.read(self._config_file)
		self._print_config()

	def reset(self):
		self.open()

	def set(self, section, key, value):
		"""Sets the dictionary value of a key in the dictionary.
		
		Args:
		    section (str): Section where the key-value pair is located.
		    key (str): Name of key paired to the value.
		    value (str): Value to set.
		"""
		if(str(section) not in self._config.sections()):
			self._log.debug('Added section \'' + str(section) + '\' to \'' + str(self._config_file) + '\'')
			self._config.add_section(str(section))

		self._log.debug('Set \'' + str(section) + '\':\'' + str(key) + '\' to \'' + str(value) + '\'')
		self._config.set(str(section), str(key), str(value))

	def save(self, file = None):
		"""Saves the loaded configuration dictionary to the requested file.
		
		Args:
		    file (str, optional): File to save data to. When unspecified, the data will be saved to the active configuration file.
		"""
		# write to file
		if not file:
			file = self._config_file
			self._log.info('Saving \'' + str(file) + '\'')
		else:
			self._log.info('Saving as \'' + str(file) + '\'')
			self._config_file = file

		with open(file, 'w') as configfile:
			self._config.write(configfile)
		
	def _print_config(self):
		"""Prints the loaded configuration dictionary for debugging.
		"""
		self._log.debug('Configuration file: \'' + str(self._config_file) + '\'')
		for section in self._config.sections():
			self._log.debug('-> \'' + str(section) + '\' = ' + str(dict(self._config[section].items())))
		self._log.debug('Configuration complete')