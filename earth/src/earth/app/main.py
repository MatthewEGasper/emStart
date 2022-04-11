import logging
import os
import qtawesome as qta
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

		# create content
		self.display = DisplayWidget(main)
		self.setCentralWidget(self.display)

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

		# start timer to update the current settings
		self.timer = QTimer()
		self.timer.timeout.connect(self.refresh)
		self.timer.start()

		# configure window
		self.setWindowTitle("Earth Emulator")
		self.setWindowIcon(qta.icon('mdi6.earth'))
		# self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.resize(800, 600)
		self.setFocusPolicy(Qt.StrongFocus)
		self.show()

	def createActions(self):
		self.openAction = QAction(qta.icon('mdi6.folder'), '&Open...', self)
		self.openAction.setStatusTip('Load configuration from file')
		self.openAction.setShortcut('Ctrl+O')
		self.openAction.triggered.connect(self.openDialog)
		
		self.saveAction = QAction(qta.icon('mdi6.content-save'), '&Save', self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip('Save configuration')
		self.saveAction.triggered.connect(lambda: self.main.config.save())
		
		self.saveAsAction = QAction(qta.icon('mdi6.content-save-settings'), '&Save As...', self)
		self.saveAsAction.setShortcut('Ctrl+Shift+S')
		self.saveAsAction.setStatusTip('Save configuration to selected file')
		self.saveAsAction.triggered.connect(self.saveAsDialog)

		self.exitAction = QAction(qta.icon('mdi6.exit-to-app'), '&Exit', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit application')
		self.exitAction.triggered.connect(QApplication.instance().quit)

		self.playAction = QAction(qta.icon('mdi6.play'), '&Play', self)
		self.playAction.setStatusTip('Resume time')
		self.playAction.triggered.connect(self.main.daemon.play)

		self.pauseAction = QAction(qta.icon('mdi6.pause'), '&Pause', self)
		self.pauseAction.setStatusTip('Suspend time')
		self.pauseAction.triggered.connect(self.main.daemon.pause)

		self.syncAction = QAction(qta.icon('mdi6.cached'), '&Sync', self)
		self.syncAction.setStatusTip('Resume from current time')
		self.syncAction.triggered.connect(self.main.daemon.sync)
		
		self.resetAction = QAction(qta.icon('mdi6.restart'), '&Reset', self)
		self.resetAction.setStatusTip('Reset configuration')
		self.resetAction.triggered.connect(self.main.reset)

		self.logAction = QAction(qta.icon('mdi6.post'), '&Open Log...', self)
		self.logAction.setStatusTip('View the program log file')
		try:
			self.logAction.triggered.connect(
				lambda: os.startfile(
					self.main.path + self.main.config.get('logging', 'file', '/logs/system.log')))
		except FileNotFoundError:
			self.log.error('The specified log file was not found')

		self.aboutAction = QAction(qta.icon('mdi6.information'), '&About', self)
		self.aboutAction.setStatusTip('Show help dialogue')
		self.aboutAction.triggered.connect(self.aboutMessage)

		self.helpAction = QAction(qta.icon('mdi6.help-circle'), '&Help', self)
		self.helpAction.setShortcut('Ctrl+H')
		self.helpAction.setStatusTip('Show help dialogue')
		self.helpAction.triggered.connect(self.helpMessage)

		self.stationAction = QAction(qta.icon('mdi6.chevron-right'), '&Update Station Configuration', self)
		self.stationAction.setStatusTip('Apply changes to station configuration')
		self.stationAction.triggered.connect(self.stationFunction)

		self.emulatorConnectAction = QAction(qta.icon('mdi6.lan-connect'), '&Connect', self)
		self.emulatorConnectAction.setStatusTip('Connect to the emulator')
		self.emulatorConnectAction.triggered.connect(self.emulatorConnectFunction)

		self.emulatorDisconnectAction = QAction(qta.icon('mdi6.lan-disconnect'), '&Disconnect', self)
		self.emulatorDisconnectAction.setStatusTip('Disconnect from the emulator')
		self.emulatorDisconnectAction.triggered.connect(self.main.controller.disconnect)

		self.graphAction = QAction(qta.icon('mdi6.chart-timeline-variant'), '&Reset Graph', self)
		self.graphAction.setStatusTip('Reset the graph')
		self.graphAction.triggered.connect(self.display._reset_graph)

	def createWidgets(self):
		self.timeWidget = QDateTimeEdit()
		self.timeWidget.setDateTime(self.main.daemon.get_time())
		self.timeWidget.setStatusTip('Set the time')
		self.timeWidget.editingFinished.connect(
			lambda: self.main.daemon.set_time(
				self.timeWidget.dateTime().toString(Qt.ISODate)))

		self.speedWidget = QSpinBox()
		self.speedWidget.setMaximum(3600)
		self.speedWidget.setMinimum(-3600)
		self.speedWidget.setValue(1)
		self.speedWidget.setStatusTip('Set the speed')
		self.speedWidget.valueChanged.connect(self.main.daemon.set_speed)

		self.latWidget = QLineEdit(self.main.config.get('station', 'latitude'))
		self.latWidget.setValidator(QDoubleValidator())
		self.latWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'station', 'latitude', self.latWidget.text()))

		self.lonWidget = QLineEdit(self.main.config.get('station', 'longitude'))
		self.lonWidget.setValidator(QDoubleValidator())
		self.lonWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'station', 'longitude', self.lonWidget.text()))

		self.eleWidget = QLineEdit(self.main.config.get('station', 'elevation'))
		self.eleWidget.setValidator(QDoubleValidator())
		self.eleWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'station', 'elevation', self.eleWidget.text()))

		self.targetWidget = QLineEdit(self.main.config.get('station', 'target'))
		self.targetWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'station', 'target', self.targetWidget.text()))

		self.portWidget = QLineEdit(self.main.config.get('emulator', 'port'))
		self.portWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'emulator', 'port', self.portWidget.text()))

		self.timeoutWidget = QLineEdit(self.main.config.get('emulator', 'timeout'))
		self.timeoutWidget.setValidator(QDoubleValidator())
		self.timeoutWidget.editingFinished.connect(
			lambda: self.main.config.set(
				'emulator', 'timeout', self.timeoutWidget.text()))

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
		editMenu.addSeparator()
		editMenu.addAction(self.resetAction)

		viewMenu = QMenu("&View", self)
		myMenuBar.addMenu(viewMenu)
		viewMenu.addAction(self.logAction)
		viewMenu.addAction(self.graphAction)

		helpMenu = QMenu("&Help", self)
		myMenuBar.addMenu(helpMenu)
		helpMenu.addAction(self.aboutAction)
		helpMenu.addAction(self.helpAction)

		self.statusBar()

	def createToolBar(self):
		# file toolbar
		fileToolBar = QToolBar("File", self)
		fileToolBar.setMovable(False)
		self.addToolBar(fileToolBar)
		fileToolBar.addAction(self.openAction)
		fileToolBar.addAction(self.saveAction)
		# edit toolbar
		editToolBar = QToolBar("Edit", self)
		self.addToolBar(editToolBar)
		editToolBar.addAction(self.playAction)
		editToolBar.addAction(self.pauseAction)
		editToolBar.addAction(self.syncAction)
		editToolBar.addAction(self.resetAction)
		# control toolbar
		controlToolBar = QToolBar("Control", self)
		self.addToolBar(controlToolBar)
		controlToolBar.addWidget(self.timeWidget)
		controlToolBar.addWidget(self.speedWidget)
		controlToolBar.addWidget(QLabel('x'))
		# station toolbar
		stationToolBar = QToolBar("Station", self)
		self.addToolBar(Qt.BottomToolBarArea, stationToolBar)
		stationToolBar.addWidget(QLabel('Latitude:'))
		stationToolBar.addWidget(self.latWidget)
		stationToolBar.addWidget(QLabel('Longitude:'))
		stationToolBar.addWidget(self.lonWidget)
		stationToolBar.addWidget(QLabel('Elevation:'))
		stationToolBar.addWidget(self.eleWidget)
		stationToolBar.addWidget(QLabel('Target:'))
		stationToolBar.addWidget(self.targetWidget)
		stationToolBar.addAction(self.stationAction)
		# emulator toolbar
		emulatorToolBar = QToolBar("Emulator", self)
		self.addToolBar(Qt.BottomToolBarArea, emulatorToolBar)
		emulatorToolBar.addWidget(QLabel('Port:'))
		emulatorToolBar.addWidget(self.portWidget)
		emulatorToolBar.addWidget(QLabel('Timeout:'))
		emulatorToolBar.addWidget(self.timeoutWidget)
		emulatorToolBar.addAction(self.emulatorConnectAction)
		emulatorToolBar.addAction(self.emulatorDisconnectAction)

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

	def refresh(self):
		self.speedWidget.setValue(self.main.daemon.get_speed())
		self.timer.start(10)

	def stationFunction(self):
		self.main.processor.reset()
		self.latWidget.setText(self.main.config.get('station', 'latitude'))
		self.lonWidget.setText(self.main.config.get('station', 'longitude'))
		self.eleWidget.setText(self.main.config.get('station', 'elevation'))
		self.targetWidget.setText(self.main.config.get('station', 'target'))

	def emulatorConnectFunction(self):
		self.main.controller.connect()
		self.portWidget.setText(self.main.config.get('emulator', 'port'))
		self.timeoutWidget.setText(self.main.config.get('emulator', 'timeout'))