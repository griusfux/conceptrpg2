from PyQt4.QtGui import *
from .ui.ArmorEditor_ui import Ui_ArmorEditor

import json

class ArmorEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = Ui_ArmorEditor()
		self.ui.setupUi(self)

		# Load up the schema file so we can get acceptable subtypes
		with open(data._schema) as f:
			subtypes = eval(json.loads(f.read())['subtype'])
		
		self.ui.subtype.addItems([i for i in subtypes])
		
		# Set the text fields
		self.ui.name.setText(data.name)
		self.ui.cost.setValue(data.cost)
		self.ui.type.setText(data.type)
		
		self.ui.subtype.setCurrentIndex(self.ui.subtype.findText(data.subtype))
		self.ui.ac.setValue(data.ac)
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.cost = self.ui.cost.value()
		self.data.subtype = self.ui.subtype.itemText(self.ui.subtype.currentIndex())
		self.data.ac = self.ui.ac.value()
