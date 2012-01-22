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
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.cost.setValue(data.cost)
		ui.description.setPlainText(data.description)
		
		ui.type.setCurrentIndex(ui.type.findText(data.type))
		ui.arcane_defense.setValue(data.arcane_defense)
		ui.physical_defense.setValue(data.physical_defense)
		ui.reflex.setValue(data.reflex)
		
	def save(self):
		ui = self.ui
		data = self.data
		
		data.name = ui.name.text()
		data.cost = ui.cost.value()
		data.description = ui.description.toPlainText()
		data.type = ui.type.itemText(ui.type.currentIndex())
		data.arcane_defense = ui.arcane_defense.value()
		data.physical_defense = ui.physical_defense.value()
		data.reflex = ui.reflex.value()
