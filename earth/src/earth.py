import logging
import sys

from app import MainWindow
from config import EarthConfig
from daemon import EarthDaemon

from PyQt6.QtWidgets import *

class Main():

	config = None
	daemon = None

	def __init__(self):
		self.config = EarthConfig()
		self.daemon = EarthDaemon(self.config)
		# self.ground = EarthProcessor() # get the current position of the target and calculate Earth position
		# self.serial = ROT2Prog() # send Earth position to hardware

if __name__ == '__main__':
	main = Main()

	app = QApplication(sys.argv)
	app.setStyle('Fusion')

	window = MainWindow(main)
	app.exec()

	main.config.save()