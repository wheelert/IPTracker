from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction, QFileDialog, QMessageBox, QLineEdit, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel
from NoteDialog import NoteDialog
from gui.addsubnet_ui import Ui_Dialog as form
from Addsubnet import Addsubnet
from IPTrackerData import IPTrackerData
from TableModel import *
from threading import Thread
import time
import os
from pathlib import Path



class MySignal(QtCore.QObject):
    ''' Why a whole new class? See here:
    https://stackoverflow.com/a/25930966/2441026 '''
    sig_no_args = QtCore.pyqtSignal()
    sig_with_str = QtCore.pyqtSignal(str)
    sig_sel_row = QtCore.pyqtSignal(int)


class UI_helper(object):
    def __init__(self):
        self._form = ""
        self.header = ['IP', 'Status', 'Hostname', 'Notes']
        self._selectedsubnetid = ""
        self.selected_QModelIndex = ""
        self.signal = MySignal()
        self.signal.sig_no_args.connect(self.tbl_update)
        self.signal.sig_sel_row.connect(self.tbl_highlight)

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
        settingsAction.setShortcut('Ctrl+A')
        settingsAction.setStatusTip('Add Subnet')
        settingsAction.triggered.connect(self.settingsCall)

        # Remove settings action
        removeAction = QAction(QIcon('remove.png'), '&Remove Subnet', app)
        removeAction.setShortcut('Ctrl+R')
        removeAction.setStatusTip('Remove Subnet')
        removeAction.triggered.connect(self.removeCall)

        # Create settings export action
        settingsAction2 = QAction(QIcon(''), '&Export', app)
        settingsAction2.setShortcut('Ctrl+E')
        settingsAction2.setStatusTip('Export')
        settingsAction2.triggered.connect(self.exportCall)

        # Create settings action
        settingsAction3 = QAction(QIcon('exit.png'), '&Scan', app)
        settingsAction3.setShortcut('Ctrl+S')
        settingsAction3.setStatusTip('Scan')
        settingsAction3.triggered.connect(self.scanCall)

        sMenu = form.menubar.addMenu('&Actions')
        sMenu.addAction(settingsAction)
        sMenu.addAction(removeAction)
        sMenu.addAction(settingsAction2)
        sMenu.addAction(settingsAction3)

    def exitCall(self):
        exit()

    def settingsCall(self):
        dialog = Addsubnet()
        dialog.exec_()
        dialog.show()
        self.poplist(self._form)

    def removeCall(self):
        # check for selected subnet
        if self._selectedsubnetid == "":
            msgbox = QMessageBox(QMessageBox.Question, "Subnet", "You must select a subnet to remove!")
            msgbox.addButton(QMessageBox.Ok)

            reply = msgbox.exec()
            return

        _name = self.selected_QModelIndex.data()
        confBox = QMessageBox()
        confBox.setIcon(QMessageBox.Question)
        confBox.setText(f"Are you sure you want to remove {_name}")
        confBox.setWindowTitle(f"Remove Subnet {_name}")
        confBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #confBox.buttonClicked.connect(msgButtonClick)

        returnValue = confBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
            Data = IPTrackerData()
            _subnet_id = Data.get_subnet_id(_name)
            Data.remove_subnet(_subnet_id)

            self.poplist(self._form)


    def exportCall(self):
        # check for selected subnet
        if self._selectedsubnetid == "":
            msgbox = QMessageBox(QMessageBox.Question, "Subnet", "You must select a subnet to export!")
            msgbox.addButton(QMessageBox.Ok)

            reply = msgbox.exec()
            return

        path = str(Path.home())

        dialog = QtWidgets.QFileDialog()
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setDirectory(path)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            _dir = dialog.selectedFiles()[0]
            _filename = self.selected_QModelIndex.data()

            Data = IPTrackerData()
            _file = Data.export_CSV(self._selectedsubnetid, _dir, _filename)
            _finishbox = QMessageBox(QMessageBox.Question, "Data Exported", "Subnet Written to file (" + _file + ")")
            _finishbox.exec()

    # populate Subnet name list
    def poplist(self, form):

        model = QtGui.QStandardItemModel()
        form.listView.setModel(model)
        form.listView.clicked.connect(self.list_click)
        Data = IPTrackerData()

        for i in Data.subnets:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)

    def list_click(self, index):
        _row = index.row()

        Data = IPTrackerData()
        _subnetid = Data.get_subnet_id(str(index.data()))

        # set vairiables
        self._selectedsubnetid = _subnetid
        self.selected_QModelIndex = index

        tblData = Data.get_ips(_subnetid)
        if len(tblData) == 0:
            tblData = [['', '', '', '']]

        tv = self._form.tableView
        tablemodel = TableModel(tblData, self.header)
        tv.setModel(tablemodel)
        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        # tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()
        tv.setSelectionBehavior(tv.SelectRows)
        # enable sorting
        tv.setSortingEnabled(False)
        tv.clicked.connect(self.subnet_click)


    def subnet_click(self, rindex):
        _col = rindex.column()
        _row = rindex.row()
        _ip = self._form.tableView.model().index(_row, 0)
        _ip = _ip.data()
        msg = [rindex.data(), _ip]

        if _col == 3:
            dlg2 = NoteDialog(msg)
            if dlg2.exec():
                Data = IPTrackerData()
                _data = (dlg2.get_note(), _ip, self._selectedsubnetid)

                Data.update_ip_note(_data)
                # update table
                self.signal.sig_no_args.emit()

            else:
                dlg2.close()

    def fping(self, address):
        import os
        import sys
        import subprocess
        import time

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd = "ping -n 1 -w 3 " + address
        else:
            cmd = ["/usr/bin/ping", "-c", "1", "-W", "3", address]

        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             startupinfo=startupinfo)

        # Wait until process terminates (without using p.wait())
        while p.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # windows
        if os.name == 'nt':
            _sub = "Received = 1"
        else:
            # linux
            _sub = "1 received,"

        # Get return code from process
        ret = p.stdout.read()
        if _sub in str(ret):
            return True
        else:
            return False

    def ipscan(self, subnetid):
        import socket

        print("subnet:" + str(subnetid))
        Data = IPTrackerData()
        _ips = Data.get_ips(subnetid)
        _cnt = 0
        for _ip in _ips:
            # Highlight row
            self.signal.sig_sel_row.emit(_cnt)
            # ping ip for status
            if self.fping(_ip[0]) == True:
                _statdata = ("Alive", _ip[0], subnetid)
                print(_statdata)
                Data.update_ip_status(_statdata)
            else:
                _statdata = ("", _ip[0], subnetid)
                Data.update_ip_status(_statdata)

            # check for dns name
            try:
                _dns = socket.gethostbyaddr(_ip[0])
                _hostname = _dns[0]
            except:
                _hostname = ""

            _data = (_hostname, _ip[0], subnetid)
            Data.update_ip_hostname(_data)

            _cnt += 1

            # update table
            self.signal.sig_no_args.emit()

    def tbl_update(self):
        self.list_click(self.selected_QModelIndex)

        print("update tbl")

    def tbl_highlight(self, row):
        tv = self._form.tableView
        tv.selectRow(row)
        print("fire highlight callback", str(row))

    def scanCall(self):
        print("scan subnet")
        # add check for no selected subnet

        t = Thread(target=self.ipscan, args=(self._selectedsubnetid,))
        t.setDaemon(True)  # set to exit with main thread
        t.start()
