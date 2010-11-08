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

		# Hook up the Add Tile button
		self.connect(self.ui.add_tile, SIGNAL('clicked()'), self.add_tile)
		
	def _create_tab(self, tiles, view):
		model = QStandardItemModel(self)
		model.setHorizontalHeaderLabels([''])
		
		for i, tile in enumerate(tiles):
			model.setItem(i, 0, QStandardItem(tile['obj']))
			
		view.setModel(model)
		
		return model
	
	def add_tile(self):
		idx = self.ui.tile_tabs.currentIndex()
		view = None
		
		# This cold probably be a bit nicer...
		if idx == 0:
			view = self.start_tiles
		elif idx == 1:
			view = self.room_tiles
		elif idx == 2:
			view = self.corridor_tiles
		elif idx == 3:
			view = self.trap_tiles
		elif idx == 4:
			view = self.end_tiles
		elif idx == 5:
			view = self.stair_tiles
		
		if view:
			view.appendRow(QStandardItem("NewTile"))
		
	def save(self):
		self.data.name = self.ui.name.text()
		self.data.encounter_deck = self.ui.encounter_deck.text()
		
		view = self.start_tiles
		self.data.start_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.room_tiles
		self.data.room_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.corridor_tiles
		self.data.corridor_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.trap_tiles
		self.data.trap_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.end_tiles
		self.data.end_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.stair_tiles
		self.data.stair_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
