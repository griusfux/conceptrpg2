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
			types = eval(json.loads(f.read())['type'])
		
		self.ui.type.addItems([i.title() for i in types])
		self.ui.hands.addItems(["One", "Two"])
		
		# Set the text fields
		self.ui.name.setText(data.name)
		self.ui.cost.setValue(data.cost)
		
		self.ui.type.setCurrentIndex(self.ui.type.findText(data.type.title()))
		self.ui.weight.setValue(data.weight)
		self.ui.range.setValue(data.range)
		self.ui.accuracy.setValue(data.accuracy)
		self.ui.hands.setCurrentIndex(data.hands-1)
#		self.ui.damage0.setValue(data.damage[0])
#		self.ui.damage1.setValue(data.damage[1])
#		self.ui.bonus.setValue(data.bonus)
		
	def save(self):
		data = self.data
		ui = self.ui
		
		data.name = ui.name.text()
		data.cost = ui.cost.value()
		
		data.type = ui.type.itemText(self.ui.type.currentIndex()).upper()
		data.weight = ui.weight.value()
		data.range = ui.range.value()
		data.accuracy = ui.accuracy.value()
		data.hands = ui.hands.currentIndex()+1
#		self.data.subtype = self.ui.subtype.itemText(self.ui.subtype.currentIndex())
#		self.data.damage = self.ui.damage0.value(), self.ui.damage1.value()
#		self.data.bonus = self.ui.bonus.value()
		