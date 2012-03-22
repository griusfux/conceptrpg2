# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide.QtGui import *
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

		# Set the text fields
		ui.name.setText(data.name)
		ui.cost.setValue(data.cost)
		ui.description.setPlainText(data.description)
		
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
		data.description = ui.description.toPlainText()
		
		data.type = ui.type.itemText(self.ui.type.currentIndex()).upper()
		data.weight = ui.weight.value()
		data.range = ui.range.value()
		data.accuracy = ui.accuracy.value()
		data.hands = ui.hands.currentIndex()+1
#		self.data.subtype = self.ui.subtype.itemText(self.ui.subtype.currentIndex())
#		self.data.damage = self.ui.damage0.value(), self.ui.damage1.value()
#		self.data.bonus = self.ui.bonus.value()
		