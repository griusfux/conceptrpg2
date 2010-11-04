from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .ui.MapEditor_ui import Ui_MapEditor

class MapEditor(QFrame):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data
		
		# Create the ui
		self.ui = Ui_MapEditor()
		self.ui.setupUi(self)
		
		# Set the text fields
		self.ui.name.setText(data.name)
		self.ui.encounter_deck.setText(data.encounter_deck)
		
		# Fill in the tile lists
		
		self.start_tiles = self._create_tab(data.start_tiles, self.ui.start_view)
		self.room_tiles = self._create_tab(data.room_tiles, self.ui.room_view)
		self.corridor_tiles = self._create_tab(data.corridor_tiles, self.ui.corridor_view)
		self.trap_tiles = self._create_tab(data.trap_tiles, self.ui.trap_view)
		self.end_tiles = self._create_tab(data.end_tiles, self.ui.end_view)
		self.stair_tiles = self._create_tab(data.stair_tiles, self.ui.stair_view)
		
		self.ui.tile_tabs.setCurrentIndex(0)

		
	def _create_tab(self, tiles, view):
		model = QStandardItemModel(self)
		model.setHorizontalHeaderLabels([''])
		
		for i, tile in enumerate(tiles):
			model.setItem(i, 0, QStandardItem(tile['obj']))
			
		view.setModel(model)
		
		return model
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.encounter_deck = self.ui.encounter_deck.text()