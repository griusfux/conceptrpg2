from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.WeaponEditor_ui import Ui_WeaponEditor

import json

class WeaponEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_WeaponEditor)
		ui = self.ui
		
		# Load up the schema file so we can get acceptable subtypes
		with open(data._schema) as f:
			types = eval(json.loads(f.read())['type'])
		
		ui.type.addItems([i.title() for i in types])
		ui.hands.addItems(["One", "Two"])
		
		# Setup the image
		image = QPixmap(data.open_image())
		data.close_image()
		ui.weapon_image.setPixmap(image)
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.cost.setValue(data.cost)
		
		ui.type.setCurrentIndex(self.ui.type.findText(data.type.title()))
		ui.weight.setValue(data.weight)
		ui.range.setValue(data.range)
		ui.accuracy.setValue(data.accuracy)
		ui.hands.setCurrentIndex(data.hands-1)
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
		