from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel
from gui.addsubnet_ui import Ui_Dialog as form
from Addsubnet import Addsubnet
from IPTrackerData import IPTrackerData
from TableModel import *
from threading import Thread 
import time

class MySignal(QtCore.QObject):
    ''' Why a whole new class? See here: 
    https://stackoverflow.com/a/25930966/2441026 '''
    sig_no_args = QtCore.pyqtSignal()
    sig_with_str = QtCore.pyqtSignal(str)
        

class UI_helper(object):
	def __init__(self):
		self._form = ""
		self.header = ['IP','Status','Hostname','Notes']
		self._selectedsubnetid = ""
		self.selected_QModelIndex = ""
		self.signal = MySignal()
		self.signal.sig_no_args.connect(self.tbl_update)
	
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
		
		# Create settings action
		settingsAction2 = QAction(QIcon('exit.png'), '&Scan', app)        
		settingsAction2.setShortcut('Ctrl+S')
		settingsAction2.setStatusTip('Scan')
		settingsAction2.triggered.connect(self.scanCall)	
	
		sMenu = form.menubar.addMenu('&Settings')
		sMenu.addAction(settingsAction)
		sMenu.addAction(settingsAction2)
		
		
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
		
		#set vairiables
		self._selectedsubnetid = _subnetid
		self.selected_QModelIndex = index
		
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
		
	def ipscan(self, subnetid):
		import socket 
		
		print("subnet:"+str(subnetid))
		Data = IPTrackerData()
		_ips = Data.get_ips(subnetid)
		for _ip in _ips:
			
			try:
				_dns = socket.gethostbyaddr(_ip[0])
				_hostname = _dns[0]
			except: 
				_hostname = ""
				
			#print("IP: "+_ip[0] + " hostname: " + _hostname)
			_data = (_hostname,_ip[0],subnetid)
			Data.update_ip_hostname(_data)
			self.signal.sig_no_args.emit()
			
			
	def tbl_update(self):
		self.list_click(self.selected_QModelIndex)
		print("update tbl")
		
	def scanCall(self):
		print("scan subnet")
		#add check for no selected subnet
		
		t = Thread(target=self.ipscan, args=( self._selectedsubnetid, ))
		t.setDaemon(True) #set to exit with main thread
		t.start()

		
		
		

			
		
		
		
		
		