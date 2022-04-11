from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyqtgraph as pg

class DisplayWidget(QWidget):

	def __init__(self, main):
		super().__init__()

		self.main = main

		# configure the graph options
		pg.setConfigOptions(antialias = True)

		self._utc = QLabel(self)
		self._status = QLabel(self)

		# make the graph
		self.az = []
		self.el = []
		self._graph = pg.PlotWidget()
		self._graph.showGrid(x = True, y = True)
		self._data = self._graph.plot(self.az, self.el)

		info_layout = QVBoxLayout()
		info_layout.addWidget(self._utc)
		info_layout.addWidget(self._status)

		main_layout = QHBoxLayout()
		main_layout.addLayout(info_layout)
		main_layout.addWidget(self._graph)

		self.setLayout(main_layout)

		self._utc_timer = QTimer()
		self._utc_timer.timeout.connect(self._refresh_utc)
		self._utc_timer.start()

		self._status_timer = QTimer()
		self._status_timer.timeout.connect(self._refresh_status)
		self._status_timer.start()

		self._graph_timer = QTimer()
		self._graph_timer.timeout.connect(self._refresh_graph)
		self._graph_timer.start()

	def _refresh_utc(self):
		time = self.main.daemon.get_time()
		speed = self.main.daemon.get_speed()

		self._utc.setText(
			time.strftime('%I:%M:%S %p\n')
			+ time.strftime('%A, %B %d, %Y\n')
			+ 'Coordinated Universal Time (UTC, '+ str(speed) + 'x speed)')

		self._utc_timer.start(250)

	def _refresh_status(self):
		target = self.main.processor.get_target()
		az, el = self.main.processor.get_target_az_el()
		ready = self.main.processor.is_ready()
		connected = self.main.controller.is_connected()

		self._status.setText(
			'Target: ' + str(target) + '\n'
			+ 'Target Azimuth: ' + str(round(az, 1)) + '°\n'
			+ 'Target Elevation: ' + str(round(el, 1)) + '°\n\n'
			+ 'Ready? ' + str(ready) + '\n'
			+ 'Connected? ' + str(connected))
		
		self._status_timer.start(100)

	def _reset_graph(self):
		self.az = []
		self.el = []
		self._graph.clear()
		self._data = self._graph.plot(self.az, self.el)

	def _refresh_graph(self):
		az, el = self.main.processor.get_target_az_el()
		
		self.az.append(az)
		self.el.append(el)

		if(len(self.az) > int(self.main.config.get('gui', 'datapoints', 100))):
			self.az.pop(0)
			self.el.pop(0)

		self._data.setData(self.az, self.el)

		self._graph_timer.start(50)