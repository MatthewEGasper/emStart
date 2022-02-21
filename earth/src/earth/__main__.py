"""Top level of the emStart Earth emulator.
"""
import argparse
import logging
import os
import sys

from .app import MainWindow
from .config import EarthConfig
from .daemon import EarthDaemon
from .processor import EarthProcessor
from .controller import EarthController
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

class EarthEmulator():

	"""Connect the main components together.
	
	Attributes:
	    config (EarthConfig): Configuration data.
	    controller (EarthController): Serial controller.
	    daemon (EarthDaemon): Time management daemon.
	    path (str): Path to the module root for file I/O.
	    processor (EarthProcessor): Astronomy data processor.
	"""
	
	_log = logging.getLogger()
	
	path = None

	def __init__(self, config_file):
		"""Creates object and initializes children.
		
		Args:
		    config_file (str): File useed to configure the application.
		"""
		# get the root path
		self.path = os.path.abspath(__file__)
		for i in range(3):
			self.path = os.path.dirname(self.path)
		# configuration file
		self.config = EarthConfig(config_file)
		# time management daemon
		self.daemon = EarthDaemon()
		# data processor
		self.processor = EarthProcessor(self)
		# serial communication
		self.controller = EarthController(self)

	def reset(self):
		"""Reset values from configuration file.
		"""
		self.daemon.reset()
		self.config.reset()
		self.processor.reset()
		self.controller.reset()

if __name__ == '__main__':
	# parse command line arguments
	parser = argparse.ArgumentParser(
		description = 'Run the emStart Earth emulator.')
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
	main = EarthEmulator(args.config_file)

	# launch gui if desired
	if args.nogui:
		print('no gui selected')
		main.config.save()
	else:
		QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		app = QApplication(sys.argv)
		app.setStyle('Fusion')
		app.setAttribute(Qt.AA_UseHighDpiPixmaps)
		window = MainWindow(main)
		app.exec()