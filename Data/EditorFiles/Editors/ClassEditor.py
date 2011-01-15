from PyQt4.QtGui import *
from .ui.ClassEditor_ui import Ui_ClassEditor

class ClassEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = Ui_ClassEditor()
		self.ui.setupUi(self)
		
		# Set the text fields
		self.ui.name.setText(data.name)
		
	def save(self):
		self.data.name = self.ui.name.text()