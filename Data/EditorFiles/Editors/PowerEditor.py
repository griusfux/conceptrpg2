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
		
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.element = self.ui.element.itemText(self.ui.element.currentIndex()).upper()
		self.data.delivery = self.ui.delivery.itemText(self.ui.delivery.currentIndex()).upper()
		self.data.effect_shape = self.ui.effect_shape.itemText(self.ui.effect_shape.currentIndex()).upper()
		self.data.shape_modifier = self.ui.shape_modifier.value()
		self.data.distance = self.ui.distance.value()
		self.data.tier = self.ui.tier.value()
		self.data.cool_down = self.ui.cool_down.value()
		self.data.description = self.ui.description.toPlainText()		
		