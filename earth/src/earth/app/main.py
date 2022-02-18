import logging
import os
import sys
import time

from .display import DisplayWidget

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
	
	def __init__(self, main):
		super().__init__()

		self.main = main
		self.log = logging.getLogger(__name__)

		# show the splash screen while loading
		splash = QLabel()
		pixmap = QPixmap(self.main.path + '/src/earth/app/assets/erau.png').scaled(300, 300)
		splash.setPixmap(pixmap)
		splash.resize(pixmap.width(),pixmap.height())
		splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		splash.setAttribute(Qt.WA_TranslucentBackground)
		splash.setAttribute(Qt.WA_DeleteOnClose)
		splash.show()

		# create content
		display = DisplayWidget(main)
		self.setCentralWidget(display)

		# create Actions
		self.createActions()
		# create Widgets
		self.createWidgets()
		# create MenuBar
		self.createMenuBar()
		# create ToolBar
		self.createToolBar()

		while not self.main.processor.is_ready():
			pass

		splash.close()

		# configure window
		self.setWindowTitle("Earth Emulator")
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.resize(QSize(0, 0))
		self.show()

	def createActions(self):
		self.openAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)), '&Open...', self)
		self.openAction.setStatusTip('Load configuration from file')
		self.openAction.setShortcut('Ctrl+O')
		self.openAction.triggered.connect(self.openDialog)
		
		self.saveAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)), '&Save', self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip('Save configuration')
		self.saveAction.triggered.connect(lambda: self.main.config.save())
		
		self.saveAsAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon)), '&Save As...', self)
		self.saveAsAction.setShortcut('Ctrl+Shift+S')
		self.saveAsAction.setStatusTip('Save configuration to selected file')
		self.saveAsAction.triggered.connect(self.saveAsDialog)

		self.exitAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_BrowserStop)), '&Exit', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit application')
		self.exitAction.triggered.connect(QApplication.instance().quit)

		self.playAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaPlay)), '&Play', self)
		self.playAction.setStatusTip('Resume time')
		self.playAction.triggered.connect(self.main.daemon.play)

		self.pauseAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaPause)), '&Pause', self)
		self.pauseAction.setStatusTip('Suspend time')
		self.pauseAction.triggered.connect(self.main.daemon.pause)

		self.syncAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_CommandLink)), '&Sync', self)
		self.syncAction.setStatusTip('Resume from current time')
		self.syncAction.triggered.connect(self.main.daemon.sync)
		
		self.resetAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_CommandLink)), '&Reset', self)
		self.resetAction.setStatusTip('Reset configuration')
		self.resetAction.triggered.connect(self.main.reset)

		self.logAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView)), '&Open Log...', self)
		self.logAction.setStatusTip('View the program log file')
		try:
			self.logAction.triggered.connect(lambda: os.startfile(self.main.path + self.main.config.get('logging', 'file', '/logs/system.log')))
		except FileNotFoundError:
			self.log.error('Log file failed to open')

		self.aboutAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation)), '&About', self)
		self.aboutAction.setStatusTip('Show help dialogue')
		self.aboutAction.triggered.connect(self.aboutMessage)

		self.helpAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion)), '&Help', self)
		self.helpAction.setShortcut('Ctrl+H')
		self.helpAction.setStatusTip('Show help dialogue')
		self.helpAction.triggered.connect(self.helpMessage)

	def createWidgets(self):
		self.speedWidget = QSlider(Qt.Horizontal, self)
		self.speedWidget.setMaximum(3600)
		self.speedWidget.setMinimum(-3600)
		self.speedWidget.setTickInterval(1)
		self.speedWidget.setTickPosition(0)
		self.speedWidget.valueChanged.connect(self.main.daemon.set_speed)

	def createMenuBar(self):
		myMenuBar = QMenuBar(self)
		self.setMenuBar(myMenuBar)

		# file menu
		fileMenu = QMenu("&File", self)
		myMenuBar.addMenu(fileMenu)
		fileMenu.addAction(self.openAction)
		fileMenu.addAction(self.saveAction)
		fileMenu.addAction(self.saveAsAction)
		fileMenu.addAction(self.exitAction)

		# edit menu
		editMenu = QMenu("&Edit", self)
		myMenuBar.addMenu(editMenu)
		editMenu.addAction(self.playAction)
		editMenu.addAction(self.pauseAction)
		editMenu.addAction(self.syncAction)
		editMenu.addAction(self.resetAction)

		viewMenu = QMenu("&View", self)
		myMenuBar.addMenu(viewMenu)
		viewMenu.addAction(self.logAction)

		helpMenu = QMenu("&Help", self)
		myMenuBar.addMenu(helpMenu)
		helpMenu.addAction(self.aboutAction)
		helpMenu.addAction(self.helpAction)

		self.statusBar()

	def createToolBar(self):
		fileToolBar = self.addToolBar("File")
		fileToolBar.addAction(self.openAction)
		fileToolBar.addAction(self.saveAction)
		# Edit toolbar
		editToolBar = QToolBar("Edit", self)
		self.addToolBar(editToolBar)
		editToolBar.addAction(self.playAction)
		editToolBar.addAction(self.pauseAction)
		editToolBar.addAction(self.syncAction)
		editToolBar.addAction(self.resetAction)
		editToolBar.addWidget(self.speedWidget)

	def saveAsDialog(self):
		filename, filter = QFileDialog.getSaveFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Select save file',
			filter  = 'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.save(filename)

	def openDialog(self):
		filename, filter = QFileDialog.getOpenFileName(
			parent = self,
			directory = self.main.path + '/config',
			caption = 'Open file',
			filter  =  'INI (*.cfg;*.conf;*.inf;*.ini;*.lng;*.url;*..buckconfig;*..flowconfig;*..hgrc)')

		if filename:
			self.main.config.open(filename)

	def aboutMessage(self):
		msg = QMessageBox()
		msg.setWindowFlags(Qt.WindowStaysOnTopHint)
		msg.setWindowTitle('About')
		msg.setText('emStart Earth Emulator Information')
		msg.setInformativeText('Author: <a href="https://github.com/tj-scherer">tj-scherer</a><br>Documentation: <a href="https://github.com/MatthewEGasper/emStart/tree/main/earth">emStart</a>')
		msg.setStandardButtons(QMessageBox.Close)
		msg.exec()

	def helpMessage(self):
		msg = QMessageBox()
		msg.setWindowFlags(Qt.WindowStaysOnTopHint)
		msg.setWindowTitle('Help')
		msg.setText('emStart Earth Emulator Help')
		msg.setInformativeText('Please refer to the documentation in <a href="https://github.com/MatthewEGasper/emStart/tree/main/earth">emStart/earth</a>')
		msg.setStandardButtons(QMessageBox.Close)
		msg.exec()