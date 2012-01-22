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
from .ui.ClassEditor_ui import Ui_ClassEditor

from Scripts.packages import Armor, Weapon

class ClassEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_ClassEditor)
		ui = self.ui
		
		# Fill combo boxes
		ui.starting_armor.addItems([i.name for i in Armor.get_package_list()])
		ui.starting_weapon.addItems([i.name for i in Weapon.get_package_list()])
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.starting_armor.setCurrentIndex(ui.starting_armor.findText(data.starting_armor))
		ui.starting_weapon.setCurrentIndex(ui.starting_weapon.findText(data.starting_weapon))
		
	def save(self):
		data = self.data
		ui = self.ui

		data.name = ui.name.text()
		data.starting_armor = ui.starting_armor.currentText()
		data.starting_weapon = ui.starting_weapon.currentText()
		