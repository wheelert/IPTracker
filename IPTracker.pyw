'''#!/user/bin/python3
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QIcon
import sys
from gui.design_ui import Ui_MainWindow
from IPTrackerData import IPTrackerData
from UI_helper import UI_helper
from Addsubnet import Addsubnet


class IPTracker(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(IPTracker, self).__init__(parent=None)
		
		Ui_MainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.setupUi(self)
		
	
def main():
	app = QApplication(sys.argv)
	form = IPTracker()
	uihelper = UI_helper()
	uihelper.build_menubar(form, app)
	
	uihelper.poplist(form)
	
	form.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
