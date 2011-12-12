from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.StatusEditor_ui import Ui_StatusEditor

class StatusEditor(BaseEditor):
	pyfile = "power.py"
	
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_StatusEditor)
		ui = self.ui
		
		# Setup the values
		ui.name.setText(data.name)
		
	def save(self):
		data = self.data
		ui = self.ui
		
		data.name = ui.name.text()