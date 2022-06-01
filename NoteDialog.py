from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QAction, QFileDialog, QMessageBox, QLineEdit, QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class NoteDialog(QDialog):

    def __init__(self, msg):
        super().__init__()

        self.setWindowTitle("Add Note")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        curNote = str( msg[0] )
        message = QLabel("Enter a note for "+str(msg[1]))
        self.layout.addWidget(message)
        self._note = QLineEdit()
        if curNote:
            self._note.setText(msg[0])

        self.layout.addWidget(self._note)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def get_note(self):
        return self._note.text()