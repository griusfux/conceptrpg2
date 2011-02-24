from PyQt4.QtGui import *
from .ui.MonsterEditor_ui import Ui_MonsterEditor

class MonsterEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data

		# Create the ui
		self.ui = Ui_MonsterEditor()
		self.ui.setupUi(self)
		
		# Setup the values
		self.ui.name.setText(data.name)
		
	def save(self):
		self.data.name = self.ui.name.text()