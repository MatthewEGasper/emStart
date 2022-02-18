from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ControlWidget(QWidget):

	def __init__(self, main):
		super().__init__()

		self._main = main

		self._time_edit = QDateTimeEdit()

		self._time_edit_button = QPushButton('>', self)
		self._time_edit_button.clicked.connect(self._set_time)

		# manual controls

		self._play_button = QPushButton('Play', self)
		self._play_button.clicked.connect(self._play_toggle)

		self._speed_slider = QSlider(Qt.Horizontal, self)
		self._speed_slider.setMaximum(3600)
		self._speed_slider.setMinimum(-3600)
		self._speed_slider.setTickInterval(1)
		self._speed_slider.setTickPosition(0)
		self._speed_slider.valueChanged.connect(self._main.daemon.set_speed)

		self._sync_button = QPushButton('Sync', self)
		self._sync_button.setShortcut('F5')
		self._sync_button.clicked.connect(self.sync)

		self._lat_text = QLineEdit()

		self._lon_text = QLineEdit()

		self._ele_text = QLineEdit()

		self._target_text = QLineEdit()

		self._apply_button = QPushButton('Apply', self)
		self._apply_button.clicked.connect(self._main.processor.reset)

		layout = QGridLayout()
		layout.addWidget(QLabel('Edit the current time:'), 0, 0)
		layout.addWidget(self._time_edit, 1, 0,)
		layout.addWidget(self._time_edit_button, 1, 1)
		layout.addWidget(QLabel('Set the speed:'), 2, 0)
		layout.addWidget(self._speed_slider, 3, 0)
		layout.addWidget(self._play_button, 4, 0)
		layout.addWidget(self._sync_button, 4, 1)
		layout.addWidget(self._lat_text, 5, 0)
		layout.addWidget(self._target_text, 5, 1)
		layout.addWidget(self._lon_text, 6, 0)
		layout.addWidget(self._apply_button, 6, 1, 7, 1)
		layout.addWidget(self._ele_text, 7, 0)

		self.setLayout(layout)

		self._refresh_timer = QTimer()
		self._refresh_timer.timeout.connect(self._refresh)
		self._refresh_timer.start()

	def _refresh(self):
		if self._main.daemon.is_playing():
			self._play_button.setText('Pause')
		else:
			self._play_button.setText('Play')
		self._speed_slider.setValue(self._main.daemon.get_speed())
		self._refresh_timer.start(10)

	def _set_time(self):
		self._main.daemon.set_time(self._time_edit.dateTime().toString(Qt.ISODate))

	def play(self):
		self._main.daemon.play()

	def pause(self):
		self._main.daemon.pause()

	def _play_toggle(self):
		if not self._main.daemon.is_playing():
			self._main.daemon.play()
		else:
			self._main.daemon.pause()

	def sync(self):
		self._main.daemon.set_speed()
		self._main.daemon.set_time()
		if not self._main.daemon.is_playing():
			self._main.daemon.play()