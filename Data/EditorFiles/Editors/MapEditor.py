# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide.QtGui import *
from PySide.QtCore import *
from .BaseEditor import BaseEditor
from .ui.MapEditor_ui import Ui_MapEditor

class MapEditor(BaseEditor):
	def __init__(self, parent, data):
		BaseEditor.__init__(self, parent, data, Ui_MapEditor)
		ui = self.ui
		
		# Set the text fields
		ui.name.setText(data.name)
		ui.encounter_deck.setText(data.encounter_deck)
		
		# Fill in the tile lists
		
		self.start_tiles = self._create_tab(data.start_tiles, ui.start_view)
		self.room_tiles = self._create_tab(data.room_tiles, ui.room_view)
		self.corridor_tiles = self._create_tab(data.corridor_tiles, ui.corridor_view)
		self.end_tiles = self._create_tab(data.end_tiles, ui.end_view)
		self.stair_tiles = self._create_tab(data.stair_tiles, ui.stair_view)
		
		ui.tile_tabs.setCurrentIndex(0)

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
		
		# This could probably be a bit nicer...
		if idx == 0:
			view = self.start_tiles
		elif idx == 1:
			view = self.room_tiles
		elif idx == 2:
			view = self.corridor_tiles
		elif idx == 3:
			view = self.end_tiles
		elif idx == 4:
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
		view = self.end_tiles
		self.data.end_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
		view = self.stair_tiles
		self.data.stair_tiles = [{"obj": view.itemFromIndex(view.index(i, 0)).text()} for i in range(view.rowCount())]
