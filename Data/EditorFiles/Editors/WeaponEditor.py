from PyQt4.QtGui import *
from .ui.WeaponEditor_ui import Ui_WeaponEditor

import json

class WeaponEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = Ui_WeaponEditor()
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
		self.ui.damage0.setValue(data.damage[0])
		self.ui.damage1.setValue(data.damage[1])
		self.ui.bonus.setValue(data.bonus)
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.cost = self.ui.cost.value()
		self.data.subtype = self.ui.subtype.itemText(self.ui.subtype.currentIndex())
		self.data.damage = self.ui.damage0.value(), self.ui.damage1.value()
		self.data.bonus = self.ui.bonus.value()
		