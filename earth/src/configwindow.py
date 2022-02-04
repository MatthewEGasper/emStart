from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer,QDateTime

class ConfigWindow(QWidget):

	def __init__(self, main):
		super().__init__()

		self.main = main

		self.label = QLabel(self)

		self.timer=QTimer()
		self.timer.timeout.connect(self.update)
		self.update()

		# button = QPushButton(self)
		# button.setText("Press me!")
		# button.setCheckable(True)
		# button.clicked.connect(self.the_button_was_clicked)
		# button.clicked.connect(self.the_button_was_toggled)

	# def the_button_was_clicked(self):
	# 	print("Clicked!")

	# def the_button_was_toggled(self, checked):
	# 	print("Checked?", checked)

	def update(self):
		self.label.setText(str(self.main.daemon.get_time()))
		self.timer.start(10)