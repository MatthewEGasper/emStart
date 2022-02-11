from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class ConfigWidget(QWidget):

	def __init__(self, earth):
		super().__init__()

		self.earth = earth

		self._time_label = QLabel(self)

		# QTimeEdit

		# manual controls

		self._play_button = QPushButton('Play', self)
		self._play_button.setCheckable(True)
		self._play_button.clicked.connect(self._play)

		self._sync_button = QPushButton('Sync', self)
		self._sync_button.setShortcut('F5')
		self._sync_button.clicked.connect(self._sync)

		layout = QVBoxLayout()

		layout.addWidget(self._time_label)
		# layout.addWidget(self._time_edit)
		# layout.addWidget(ManualControls(self.earth))
		layout.addWidget(self._play_button)
		layout.addWidget(self._sync_button)

		self.setLayout(layout)

		self._timer = QTimer()
		self._timer.timeout.connect(self._time_refresh)
		self._timer.start()

	def _play(self, play):
		if play:
			self.earth.daemon.play()
			self._play_button.setText('Pause')
		else:
			self.earth.daemon.pause()
			self._play_button.setText('Play')

	def _sync(self):
		self.earth.daemon.set_time()
		if not self._play_button.isChecked():
			self._play_button.click()

	def _time_refresh(self):
		time = self.earth.daemon.get_time()
		self._time_label.setText(str(time.date()) + '\n' + str(time.time()))
		self._timer.start(10)