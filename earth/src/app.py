import sys

from configwindow import ConfigWindow
from viewerwindow import ViewerWindow

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
	def __init__(self, main):
		super().__init__()

		# configure window
		self.setMinimumSize(QSize(720, 480))
		self.setWindowTitle("emStart Earth Controller")
		self._menu()

		layout = QHBoxLayout()

		layout.addWidget(ConfigWindow(main))
		layout.addWidget(ViewerWindow(main))

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		self.show()

	def _menu(self):
		self._file_menu()
		self._edit_menu()
		self._view_menu()
		self._help_menu()
		self.statusBar()

	def _file_menu(self):
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QApplication.instance().quit)

		menu = self.menuBar().addMenu('&File')
		menu.addAction(exitAction)

	def _edit_menu(self):
		menu = self.menuBar().addMenu('&Edit')
		# menu.addAction(exitAction)

	def _view_menu(self):
		menu = self.menuBar().addMenu('&View')
		# menu.addAction(exitAction)

	def _help_menu(self):
		menu = self.menuBar().addMenu('&Help')
		# menu.addAction(exitAction)