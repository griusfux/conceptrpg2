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
		self.ui.ai_start_state.setText(data.ai_start_state)
		self.ui.ai_keywords.insertItems(0, data.ai_keywords)
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.ai_start_state = self.ui.ai_start_state.text()