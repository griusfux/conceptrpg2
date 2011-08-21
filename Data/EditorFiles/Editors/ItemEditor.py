from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.ItemEditor_ui import Ui_ItemEditor

class ItemEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_ItemEditor)
		
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