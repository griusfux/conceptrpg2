from PyQt4.QtGui import *
from .ui.PowerEditor_ui import Ui_PowerEditor

import json

class PowerEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = Ui_PowerEditor()
		self.ui.setupUi(self)
		
		# Load up the schema file so we can get acceptable subtypes
		with open(data._schema) as f:
			range_type = eval(json.loads(f.read())['range_type'])
		
		self.ui.range_type.addItems([i for i in range_type])
		
		# Set the input fields
		self.ui.name.setText(data.name)
		self.ui.range_type.setCurrentIndex(self.ui.range_type.findText(data.range_type))
		self.ui.range_size.setValue(data.range_size)
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.range_type = self.ui.range_type.itemText(self.ui.range_type.currentIndex())
		self.data.range_size = self.ui.range_size.value()
		