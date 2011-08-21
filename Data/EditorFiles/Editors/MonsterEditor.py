from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.MonsterEditor_ui import Ui_MonsterEditor

class MonsterEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_MonsterEditor)
		ui = self.ui
		
		# Setup the values
		ui.name.setText(data.name)
		
	def save(self):
		self.data.name = self.ui.name.text()