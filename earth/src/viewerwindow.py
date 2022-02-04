from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtGui import QIcon, QAction

class ViewerWindow(QWidget):

	def __init__(self, main):
		super().__init__()

		button = QPushButton(self)
		button.setText("Press me too!")
		button.setCheckable(True)
		button.clicked.connect(self.the_button_was_clicked)
		button.clicked.connect(self.the_button_was_toggled)
		pass

	def the_button_was_clicked(self):
		print("Clicked too!")

	def the_button_was_toggled(self, checked):
		print("Checked too?", checked)