from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class ConfigWindow(QWidget):

	def __init__(self, main):
		super().__init__()

		self.main = main
		self.timer = QTimer()
		self.timer.timeout.connect(self.refresh)
		self.timer.start()

		self.time_label = QLabel(self)

		self.play_button = QPushButton('Play', self)
		self.play_button.setCheckable(True)
		self.play_button.clicked.connect(self.play)

		self.sync_button = QPushButton('Sync', self)
		self.sync_button.clicked.connect(self.sync)

		# TODO try out QTimeEdit

		layout = QVBoxLayout()

		layout.addWidget(self.time_label)
		layout.addWidget(self.play_button)
		layout.addWidget(self.sync_button)

		self.setLayout(layout)

	def play(self, play):
		if play:
			self.main.daemon.play()
			self.play_button.setText('Pause')
		else:
			self.main.daemon.pause()
			self.play_button.setText('Play')

	def sync(self):
		self.main.daemon.set_time()
		self.main.daemon.play()
		if not self.play_button.isChecked():
			self.play_button.click()

	def refresh(self):
		time = self.main.daemon.get_time()
		self.time_label.setText(str(time.date()) + '\n' + str(time.time()))
		self.timer.start(10)