from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.ArmorEditor_ui import Ui_ArmorEditor

import json

class ArmorEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_ArmorEditor)
		ui = self.ui

		# Load up the schema file so we can get acceptable types
		with open(data._schema) as f:
			types = eval(json.loads(f.read())['type'])
		
		ui.type.addItems([i for i in types])
		
		# Setup the image
		image = QPixmap(data.open_image())
		data.close_image()
		ui.armor_image.setPixmap(image)
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.cost.setValue(data.cost)
		
		ui.type.setCurrentIndex(ui.type.findText(data.type))
		ui.arcane_defense.setValue(data.arcane_defense)
		ui.physical_defense.setValue(data.physical_defense)
		ui.reflex.setValue(data.reflex)
		
	def save(self):
		ui = self.ui
		data = self.data
		
		data.name = ui.name.text()
		data.cost = ui.cost.value()
		data.type = ui.type.itemText(ui.type.currentIndex())
		data.arcane_defense = ui.arcane_defense.value()
		data.physical_defense = ui.physical_defense.value()
		data.reflex = ui.reflex.value()
