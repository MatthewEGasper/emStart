import logging
import os
import sys

from PyQt6.QtWidgets import *
from earth import *

class Earth():

	def __init__(self):
		# configuration file
		self.config = EarthConfig('../config/config.ini')

		# time management daemon
		self.daemon = EarthDaemon()

		# data processing daemon
		# self.ground = EarthProcessor(self)

		# ROT2Prog serial communication
		# self.serial = EarthController(self)

if __name__ == '__main__':
	earth = Earth()

	app = QApplication(sys.argv)
	# app.setStyle('Fusion')

	window = MainWindow(earth)
	window.show()

	app.exec()

	# earth.config.save()

	# restart the program (will need this later to reload log verbosity)
	# os.execl(sys.executable, sys.executable, *sys.argv)