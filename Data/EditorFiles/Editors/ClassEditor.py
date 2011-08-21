from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.ClassEditor_ui import Ui_ClassEditor

class ClassEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_ClassEditor)
		ui = self.ui
		
		# Set the text fields
		ui.name.setText(data.name)
		
	def save(self):
		self.data.name = self.ui.name.text()