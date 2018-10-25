from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel
from gui.addsubnet_ui import Ui_Dialog as form
from Addsubnet import Addsubnet
from IPTrackerData import IPTrackerData
from TableModel import *


class UI_helper(object):
	def __init__(self):
		self._form = ""
		self.header = ['IP','Hostname','Notes']
	
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
		form.listView.clicked.connect(self.list_click)
		Data = IPTrackerData()
		

		for i in Data.subnets:
			item = QtGui.QStandardItem(i)
			model.appendRow(item)	

	def list_click(self, index):
		_row = index.row()
		print("clicked list: " + str(_row) )
		
		
		Data = IPTrackerData()
		_subnetid = Data.get_subnet_id(str(index.data()))
		tblData = Data.get_ips(_subnetid)
		if len(tblData) == 0:
			tblData = [['','','']]
		
		tv = self._form.tableView
		tablemodel = TableModel(tblData,self.header)
		tv.setModel(tablemodel)
		# hide vertical header
		vh = tv.verticalHeader()
		vh.setVisible(False)

        # set horizontal header properties
		hh = tv.horizontalHeader()
		hh.setStretchLastSection(True)

        # set column width to fit contents
		#tv.resizeColumnsToContents()

        # set row height
		tv.resizeRowsToContents()
        # enable sorting
		tv.setSortingEnabled(False)

		

			
		
		
		
		
		