from PyQt4.QtGui import *
from .BaseEditor import BaseEditor
from .ui.MonsterEditor_ui import Ui_MonsterEditor
from ..common import get_blender_objects

from Scripts.packages import ActionSet

class MonsterEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_MonsterEditor)
		ui = self.ui
				
		# Fill combo boxes
		ui.root_object.addItems(get_blender_objects(data))
		ui.action_set.addItems([i.name for i in ActionSet.get_package_list()])
		
		# Setup the image
		image = QPixmap(data.open_image())
		data.close_image()
		ui.monster_image.setPixmap(image)
		
		# Setup the values
		ui.name.setText(data.name)
		idx = ui.root_object.findText(data.root_object)
		if idx < 0:
			ui.root_object.setEditText(data.root_object)
		else:
			ui.root_object.setCurrentIndex(ui.root_object.findText(data.root_object))
		ui.action_set.setCurrentIndex(ui.action_set.findText(data.action_set))
		
	def save(self):
		self.data.name = self.ui.name.text()
				
		data.name = ui.name.text()
		data.root_object = ui.root_object.currentText()
		data.action_set = ui.action_set.currentText()