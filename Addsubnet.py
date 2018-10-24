from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QIcon
import sys
from gui.addsubnet_ui import Ui_Dialog
from IPTrackerData import IPTrackerData


class Addsubnet(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self, parent=None):
		#super(Addsubnet, self).__init__(parent=None)
		
		QtWidgets.QDialog.__init__(self)
		self.ui = Ui_Dialog()
		self.setupUi(self)
		
		
		self.buttonBox.accepted.connect(self.subnetAdd)
	def subnetAdd(self):
		_name = self.lineEdit.text()
		_ip = self.lineEdit_2.text()
		_mask = self.lineEdit_3.text()
		
		Data = IPTrackerData()
		data = (_name,_ip,_mask)
		id = Data.create_subnet(data)
		
		print("Add:"+_name+" "+_ip+" "+_mask+"to database")
		
	
def main():
	app = QApplication(sys.argv)
	form = Addsubnet()	
	
	
	form.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
