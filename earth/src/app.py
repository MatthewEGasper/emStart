import sys

from configwindow import ConfigWindow
from viewerwindow import ViewerWindow

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
	def __init__(self, main):
		super().__init__()

		# configure window
		self.setMinimumSize(QSize(720, 480))
		self.setWindowTitle("emStart Earth")
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
		# Actions:
		# save
		# save as
		# load
		# preferences
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QApplication.instance().quit)

		menu = self.menuBar().addMenu('&File')
		menu.addAction(exitAction)

	def _edit_menu(self):
		# Actions:
		# sync time
		# set time
		# change target
		# manual control toggle
		menu = self.menuBar().addMenu('&Edit')

	def _view_menu(self):
		# Actions:
		# colors?
		# idk
		menu = self.menuBar().addMenu('&View')

	def _help_menu(self):		
		aboutAction = QAction(QIcon('../assets/about.png'), '&About', self)
		aboutAction.setStatusTip('Show help dialogue')
		aboutAction.triggered.connect(self.show_about_message)

		helpAction = QAction(QIcon('../assets/help.png'), '&Help', self)
		helpAction.setShortcut('Ctrl+H')
		helpAction.setStatusTip('Show help dialogue')
		helpAction.triggered.connect(self.show_help_message)

		menu = self.menuBar().addMenu('&Help')
		menu.addAction(aboutAction)
		menu.addAction(helpAction)

	def show_about_message(self):
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth About')
		msg.setText('Author: <a href="https://github.com/tj-scherer">tj-scherer</a>')
		msg.exec()

	def show_help_message(self):
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth Help')
		msg.setText('Please refer to the documentation in <a href="https://github.com/MatthewEGasper/emStart/tree/main/earth">emStart/earth</a>')
		msg.exec()