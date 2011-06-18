from PyQt4.QtGui import *
from .ui.ArmorEditor_ui import Ui_ArmorEditor

import json

class ArmorEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = ui = Ui_ArmorEditor()
		ui.setupUi(self)

		# Load up the schema file so we can get acceptable types
		with open(data._schema) as f:
			types = eval(json.loads(f.read())['type'])
		
		ui.type.addItems([i for i in types])
		
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
