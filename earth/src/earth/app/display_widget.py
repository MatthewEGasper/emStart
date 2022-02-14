from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DisplayWidget(QWidget):

	def __init__(self, main):
		super().__init__()

		self.main = main

		self._status_label = QLabel(self)

		layout = QVBoxLayout()

		layout.addWidget(self._status_label)

		self.setLayout(layout)

		self._refresh_timer = QTimer()
		self._refresh_timer.timeout.connect(self._refresh)
		self._refresh_timer.start()

	def _refresh(self):
		time = self.main.daemon.get_time()
		speed = self.main.daemon.get_speed()
		target = self.main.processor.get_target()
		az, el = self.main.processor.get_az_el()
		self._status_label.setText(
			time.strftime('%I:%M:%S.%f %p\n')
			+ time.strftime('%A, %B %d, %Y\n')
			+ 'Coordinated Universal Time (UTC, '+ str(speed) + 'x speed)\n\n'
			+ 'Target: ' + str(target) + '\n'
			+ 'Azimuth: ' + str(round(az, 1)) + '°\n'
			+ 'Elevation: ' + str(round(el, 1)) + '°')
		
		self._refresh_timer.start(10)