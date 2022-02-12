import logging
import os
import sys

from .config_widget import ConfigWidget
from .display_widget import DisplayWidget

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
	def __init__(self, main):
		super().__init__()

		self.main = main
		self._log = logging.getLogger(__name__)

		# configure window
		self.setMinimumSize(QSize(720, 480))
		self.setWindowTitle("emStart Earth")

		# build menu bar
		self._menu()

		# set layout and contents
		layout = QHBoxLayout()
		layout.addWidget(ConfigWidget(main))
		layout.addWidget(DisplayWidget(main))

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def _menu(self):
		self._file_menu()
		self._edit_menu()
		self._view_menu()
		self._help_menu()
		self.statusBar()

	def _cfg_saveas(self):
		filename, filter = QFileDialog.getSaveFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Select save file',
			filter  = 'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.save(filename)

	def _cfg_open(self):
		filename, filter = QFileDialog.getOpenFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Open file',
			filter  =  'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.reload(filename)

	def _file_menu(self):
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
		sync = QAction('&Synchronize', self)
		# sync time

		timeset = QAction('&Set Time...', self)
		# set time window

		target = QAction('&Change Target...', self)
		# select target window

		# manual control toggle

		cfg = QAction('&Configure...', self)
		# open new window with parameters
		
		cfg_reset = QAction('&Reset', self)
		cfg_reset.setStatusTip('Reset configuration')
		cfg_reset.triggered.connect(lambda: self.main.config.reload())

		menu = self.menuBar().addMenu('&Edit')
		menu.addAction(sync)
		menu.addAction(timeset)
		menu.addAction(target)
		menu.addAction(cfg)
		menu.addAction(cfg_reset)

	def _view_menu(self):
		# Actions:
		# colors?
		# idk
		log_open = QAction('&Open Log...', self)
		log_open.setStatusTip('View the program log file')
		try:
			log_open.triggered.connect(lambda: os.startfile(self.main.path + self.main.config.get('logging', 'file', '/logs/system.log')))
		except FileNotFoundError:
			self._log.error('Log file failed to open')

		menu = self.menuBar().addMenu('&View')
		menu.addAction(log_open)

	def _help_menu(self):		
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
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth About')
		msg.setText('Author: <a href="https://github.com/tj-scherer">tj-scherer</a>')
		msg.exec()

	def _show_help_message(self):
		msg = QMessageBox()
		msg.setWindowTitle('emStart Earth Help')
		msg.setText('Please refer to the documentation in <a href="https://github.com/MatthewEGasper/emStart/tree/main/earth">emStart/earth</a>')
		msg.exec()