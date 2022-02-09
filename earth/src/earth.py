"""Summary
"""
import logging
import sys

from app import MainWindow
from config import EarthConfig
from daemon import EarthDaemon
from rot2prog import ROT2Prog


from PyQt6.QtWidgets import *

class Earth():

	"""Summary
	
	Attributes:
	    config (TYPE): Description
	    daemon (TYPE): Description
	"""
	
	def __init__(self):
		"""Summary
		"""
		self.config = EarthConfig()
		self.daemon = EarthDaemon(self.config)
		# set placeholders for objects which must be created later
		self.serial = None
		self.ground = None

if __name__ == '__main__':
	earth = Earth()

	app = QApplication(sys.argv)
	app.setStyle('Fusion')

	window = MainWindow(earth)
	window.show()
	app.exec()
	earth.config.save()