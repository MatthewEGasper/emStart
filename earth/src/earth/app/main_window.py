"""The top leve of the PyQt user interface.
"""
import logging
import os
import sys

from .control_widget import ControlWidget
from .display_widget import DisplayWidget

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

	"""Main PyQt user interface.
	
	Attributes:
			main (Earth): Top level object used for function calls.
	"""
	
	def __init__(self, main):
		"""Creates object and sets layout.
		
		Args:
				main (Earth): Top level object used for function calls.
		"""
		super().__init__()

		self.main = main
		self._log = logging.getLogger(__name__)

		# configure window
		self.setMinimumSize(QSize(720, 480))
		self.setWindowTitle("emStart Earth Controller")

		# create content
		self.control_widget = ControlWidget(main)
		self.display_widget = DisplayWidget(main)

		# build menu bar
		self._menu()

		# set layout and contents
		layout = QHBoxLayout()
		layout.addWidget(self.control_widget, 1)
		layout.addWidget(self.display_widget, 2)

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

		while not self.main.processor.ready:
			pass
		self.show()

	def _menu(self):
		"""Add the menu bar to the user interface.
		"""
		self._file_menu()
		self._edit_menu()
		self._view_menu()
		self._help_menu()
		self.statusBar()

	def _cfg_saveas(self):
		"""Open the file dialog to select a save file.
		"""
		filename, filter = QFileDialog.getSaveFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Select save file',
			filter  = 'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.save(filename)

	def _cfg_open(self):
		"""Open a file dialog to select an open file.
		"""
		filename, filter = QFileDialog.getOpenFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Open file',
			filter  =  'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.reload(filename)

	def _file_menu(self):
		"""Set up the file submenu.
		"""
		cfg_open = QAction('&Open...', self)
		cfg_open.setStatusTip('Load configuration from file')
		cfg_open.setShortcut('Ctrl+O')
		cfg_open.triggered.connect(self._cfg_open)
		
		cfg_save = QAction('&Save', self)
		cfg_save.setShortcut('Ctrl+S')
		cfg_save.setStatusTip('Save configuration')
		cfg_save.triggered.connect(lambda: self.main.config.save())
		
		cfg_saveas = QAction('&Save As...', self)
		cfg_saveas.setShortcut('Ctrl+Shift+S')
		cfg_saveas.setStatusTip('Save configuration to selected file')
		cfg_saveas.triggered.connect(self._cfg_saveas)

		restart = QAction('&Restart', self)
		restart.setStatusTip('Restart application')
		restart.triggered.connect(self.main.restart)

		exit = QAction('&Exit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		exit.triggered.connect(QApplication.instance().quit)

		menu = self.menuBar().addMenu('&File')
		menu.addAction(cfg_open)
		menu.addAction(cfg_save)
		menu.addAction(cfg_saveas)
		menu.addAction(restart)
		menu.addAction(exit)

	def _edit_menu(self):
		"""Set up the edit submenu.
		"""
		play = QAction('&Play', self)
		play.setStatusTip('Resume time')
		play.triggered.connect(self.main.daemon.play)

		pause = QAction('&Pause', self)
		pause.setStatusTip('Suspend time')
		pause.triggered.connect(self.main.daemon.pause)

		sync = QAction('&Sync', self)
		sync.setStatusTip('Resume from current time')
		sync.triggered.connect(self.control_widget.sync)
		
		reset = QAction('&Reset', self)
		reset.setStatusTip('Reset configuration')
		reset.triggered.connect(self.main.reset)

		menu = self.menuBar().addMenu('&Edit')
		menu.addAction(play)
		menu.addAction(pause)
		menu.addAction(sync)
		menu.addAction(reset)

	def _view_menu(self):
		"""Set up the view submenu.
		"""
		log_open = QAction('&Open Log...', self)
		log_open.setStatusTip('View the program log file')
		try:
			log_open.triggered.connect(lambda: os.startfile(self.main.path + self.main.config.get('logging', 'file', '/logs/system.log')))
		except FileNotFoundError:
			self._log.error('Log file failed to open')

		menu = self.menuBar().addMenu('&View')
		menu.addAction(log_open)

	def _help_menu(self):		
		"""Set up the help submenu.
		"""
		about = QAction('&About', self)
		about.setStatusTip('Show help dialogue')
		about.triggered.connect(self._show_about_message)

		help = QAction('&Help', self)
		help.setShortcut('Ctrl+H')
		help.setStatusTip('Show help dialogue')
		help.triggered.connect(self._show_help_message)

		menu = self.menuBar().addMenu('&Help')
		menu.addAction(about)
		menu.addAction(help)

	def _show_about_message(self):
		"""Show the about message.
		"""
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth About')
		msg.setText('Author: <a href="https://github.com/tj-scherer">tj-scherer</a>')
		msg.exec()

	def _show_help_message(self):
		"""Show the help message.
		"""
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth Help')
		msg.setText('Please refer to the documentation in <a href="https://github.com/MatthewEGasper/emStart/tree/main/earth">emStart/earth</a>')
		msg.exec()