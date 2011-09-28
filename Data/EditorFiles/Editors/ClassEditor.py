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
		