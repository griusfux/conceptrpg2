from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.PowerEditor_ui import Ui_PowerEditor

import json

class PowerEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_PowerEditor)
		ui = self.ui
		
		# Load up the schema file so we can get acceptable subtypes
		with open(data._schema) as f:
			schema = json.loads(f.read())
			element = eval(schema['element'])
			delivery = eval(schema['delivery'])
			effect_shape = eval(schema['effect_shape'])
			
		
		ui.element.addItems([i.title() for i in element])
		ui.delivery.addItems([i.title() for i in delivery])
		ui.effect_shape.addItems([i.title() for i in effect_shape])
		
		# Set the input fields
		ui.name.setText(data.name)
		ui.element.setCurrentIndex(ui.element.findText(data.element.title()))
		ui.delivery.setCurrentIndex(ui.delivery.findText(data.delivery.title()))
		ui.effect_shape.setCurrentIndex(ui.effect_shape.findText(data.effect_shape.title()))
		ui.shape_modifier.setValue(data.shape_modifier)
		ui.distance.setValue(data.distance)
		ui.tier.setValue(data.tier)
		ui.cool_down.setValue(data.cool_down)
		ui.description.setPlainText(data.description)
		
		# Setup target mask
		ui.tm_self.setChecked("SELF" in data.target_mask)
		ui.tm_enemies.setChecked("ENEMIES" in data.target_mask)
		ui.tm_allies.setChecked("ALLIES" in data.target_mask)
		
		
	def save(self):
		data = self.data
		ui = self.ui
		
		data.name = ui.name.text()
		data.element = ui.element.itemText(ui.element.currentIndex()).upper()
		data.delivery = ui.delivery.itemText(ui.delivery.currentIndex()).upper()
		data.effect_shape = ui.effect_shape.itemText(ui.effect_shape.currentIndex()).upper()
		data.shape_modifier = ui.shape_modifier.value()
		data.distance = ui.distance.value()
		data.tier = ui.tier.value()
		data.cool_down = ui.cool_down.value()
		data.description = ui.description.toPlainText()
		
		# Handle the target mask
		tm = []
			
		if ui.tm_self.isChecked(): tm.append("SELF")
		if ui.tm_enemies.isChecked(): tm.append("ENEMIES")
		if ui.tm_allies.isChecked(): tm.append("ALLIES")
		
		data.target_mask = tm