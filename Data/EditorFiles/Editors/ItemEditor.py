from PyQt4.QtGui import *
from .ItemEditor_ui import Ui_ItemEditor

class ItemEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data

		# Create the ui
		self.ui = Ui_ItemEditor()
		self.ui.setupUi(self)
		
		# Set the text fields
		self.ui.name.setText(data.name)
		self.ui.cost.setValue(data.cost)
		self.ui.type.setText(data.type)
		
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.cost = self.ui.cost.value()