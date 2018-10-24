from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QIcon
from gui.addsubnet_ui import Ui_Dialog as form
from Addsubnet import Addsubnet
from IPTrackerData import IPTrackerData


class UI_helper(object):
	def __init__(self):
		self._form = ""
	
	def build_menubar(self, form, app):
		
		self._form = form
		# Create exit action
		exitAction = QAction(QIcon('exit.png'), '&Exit', app)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.exitCall)	
	
		fileMenu = form.menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		
		# Create settings action
		settingsAction = QAction(QIcon('exit.png'), '&Add Subnet', app)        
		settingsAction.setShortcut('Ctrl+S')
		settingsAction.setStatusTip('Add Subnet')
		settingsAction.triggered.connect(self.settingsCall)	
	
		sMenu = form.menubar.addMenu('&Settings')
		sMenu.addAction(settingsAction)
		
		
	def exitCall(self):
		exit()
		
	def settingsCall(self):
		dialog = Addsubnet()
		dialog.exec_()
		dialog.show()
		self.poplist(self._form)
		
	def poplist(self,form):

		model = QtGui.QStandardItemModel()
		form.listView.setModel(model)
		Data = IPTrackerData()
		

		for i in Data.subnets:
			item = QtGui.QStandardItem(i)
			model.appendRow(item)	
		
		
		