from PyQt4.QtGui import *
from .ui.ItemEditor_ui import Ui_ItemEditor

class ItemEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data

		# Create the ui
		self.ui = Ui_ItemEditor()
		self.ui.setupUi(self)
		ui = self.ui
		
		# Setup the image
		image = QPixmap(data.open_image())
		data.close_image()
		ui.item_image.setPixmap(image)
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.cost.setValue(data.cost)
		
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.cost = self.ui.cost.value()