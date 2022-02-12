import argparse
import logging
import os
import sys

from .app import MainWindow
from .config import EarthConfig
from .daemon import EarthDaemon
from .processor import EarthProcessor
from .controller import EarthController
from PyQt6.QtWidgets import QApplication

class Earth():

	path = None

	def __init__(self, config_file):
		self.path = self._get_path()
		# configuration file
		self.config = EarthConfig(config_file)
		self._log = logging.getLogger()
		self._log.debug('Configuration complete')
		# time management daemon
		self.daemon = EarthDaemon()
		# data processor
		self.processor = EarthProcessor(self)
		# serial communication
		self.controller = EarthController()

	def restart(self):
		self._log.critical('Restart function not yet implemented. Please restart manually.')
		exit()

	def _get_path(self):
		path = os.path.abspath(__file__)
		for i in range(3):
			path = os.path.dirname(path)
		return path

if __name__ == '__main__':
	# parse command line arguments
	parser = argparse.ArgumentParser(
		description = 'Run the emStart Earth module.')
	parser.add_argument(
		'-c',
		metavar = 'config_file',
		dest = 'config_file',
		default = '../config/config.ini',
		help = 'path to the configuration file')
	parser.add_argument(
		'-nogui',
		action = 'store_true',
		help = 'set to run without the gui')
	args = parser.parse_args()

	# initialize the required modules
	main = Earth(args.config_file)

	# launch gui if desired
	if args.nogui:
		print('no gui')
		main.config.save()
	else:
		app = QApplication(sys.argv)
		window = MainWindow(main)
		window.show()
		app.exec()