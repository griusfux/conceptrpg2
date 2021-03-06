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

import sys
import json

from PySide.QtGui import *
from PySide.QtCore import *

from Scripts.packages import *

from .Editors import *
from .LogWidget import *
from .NewDialog import NewDialog
from .SettingsDialog import SettingsDialog

from .common import SETTINGS

	
class EditorWindow(QMainWindow):

	EDITORS = {
		'Armors': ArmorEditor,
		'Classes': ClassEditor,
		'Items': ItemEditor,
		'Maps': MapEditor,
		'Monsters': MonsterEditor,
		'Powers': PowerEditor,
		'Races': RaceEditor,
		'Statuses': StatusEditor,
		'Weapons': WeaponEditor,
		}

	def __init__(self):
		QMainWindow.__init__(self)
		
		# Window
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('Editor')
		
		# Logger
		logger = LogWidget(self)
		
		# Load up saved settings if there are any
		self.load_settings()
		
		# Menu
		new = QAction('&New', self)
		new.setShortcut('Ctrl+N')
		new.setStatusTip('Create a new package')
		self.connect(new, SIGNAL('triggered()'), self.new_file)
		
		save = QAction('&Save', self)
		save.setShortcut('Ctrl+S')
		save.setStatusTip('Save the currently selected package')
		self.connect(save, SIGNAL('triggered()'), self.save_file)
		
		settings = QAction('Settings', self)
		save.setStatusTip('Change settings')
		self.connect(settings, SIGNAL('triggered()'), self.open_settings)
		
		exit = QAction('E&xit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit the application')
		self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))
		
		file = self.menuBar().addMenu('&File')
		file.addAction(new)
		file.addAction(save)
		file.addAction(settings)
		file.addAction(exit)
		
		# The current editor
		
		self.editor = QFrame(self)
		self.editor.setFrameShape(QFrame.StyledPanel)
		
		# Widgets

		splitter = QSplitter(self)
		splitter.setChildrenCollapsible(False)
				
		# Tree
		model = QStandardItemModel(self)
		self.root = model.invisibleRootItem()
		
		self.data_files = {}
		
		# Create the sub trees
		# XXX uncomment subtrees when they are ready
		self.create_subtree('Armors', Armor)
		self.create_subtree('Classes', Class)
		self.create_subtree('Decks', EncounterDeck)
		self.create_subtree('Items', Item)
		self.create_subtree('Maps', Map)
		self.create_subtree('Monsters', Monster)
		self.create_subtree('Powers', Power)
		self.create_subtree('Races', Race)
		# self.create_subtree('Shields', Shield)
		self.create_subtree('Statuses', Status)
		self.create_subtree('Weapons', Weapon)
		
		left = QTreeView()
		left.setHeaderHidden(True)
		left.setModel(model)
		self.tree = left
		self.model = model
		self.connect(self.tree, SIGNAL('clicked(QModelIndex)'), self.tree_clicked)
		splitter.addWidget(left)
		
		right = QSplitter()
		right.setOrientation(Qt.Vertical)
		right.addWidget(self.editor)
		right.addWidget(logger)
		right.setStretchFactor(0, 40)
		right.setStretchFactor(1, 1)
		self.right = right
		
		splitter.addWidget(right)
		splitter.setStretchFactor(0, 1)
		splitter.setStretchFactor(1, 4)
		
		
		self.setCentralWidget(splitter)
		
	def new_file(self):
		dialog = NewDialog(self)
		dialog.exec()
		
	def open_settings(self):
		dialog = SettingsDialog(self)
		dialog.exec()
		
	def save_file(self):
		if hasattr(self.editor, "data"):
			print("Saving %s..." % self.editor.data.name)
			self.editor.save()
			self.editor.data.write()
			self.editor.qtitem.setForeground(Qt.black)
			
	def load_settings(self):
		try:
			f = open('editor_settings.conf')
		except IOError:
			msg = QMessageBox();
			msg.setText("No settings file found, please check your settings.")
			msg.exec()
			
			self.open_settings()
			return
		
		settings = json.loads(f.read())
		f.close()
		
		for key in SETTINGS:
			SETTINGS[key] = settings.get(key)
			
	def save_settings(self):
		with open('editor_settings.conf', 'w') as f:
			f.write(json.dumps(SETTINGS))
		
	def closeEvent(self, *args, **kwargs):
		self.save_settings()
		return QMainWindow.closeEvent(self, *args, **kwargs)
		
	def create_subtree(self, type, package):
		sub_root = QStandardItem(type)
		sub_root.setEditable(False)
		self.data_files[type] = {}
		self.root.appendRow(sub_root)
		
		# Build a list of the files to use
		files = [i.split('.')[0] for i in os.listdir(package._dir) if not i.startswith('.')]
		
		# Remove duplicates
		for file in files:
			while files.count(file) > 1:
				files.remove(file)
		
		# Load the files
		for file in files:
			if file.startswith('.'): continue
			try:
				arc_file = package(file)
			except Exception as e:
				import traceback
				traceback.print_exc()
				print('Unable to open', file)
				continue

			item =  QStandardItem(arc_file.name)
			item.setData(arc_file)
			item.setEditable(False)
			sub_root.appendRow(item)
			self.data_files[type][file] = arc_file
		
	def change_editor(self, editor):
		# Now change the editor
		editor.setFrameShape(QFrame.StyledPanel)
		self.editor = editor
		self.right.widget(0).hide()
		self.right.widget(0).deleteLater()
		self.right.insertWidget(0, editor)
		self.right.setStretchFactor(0, 40)
		self.right.setStretchFactor(1, 1)
		
			
	def tree_clicked(self, index):
		item = self.model.itemFromIndex(index)
		
		if item.parent():
			text = item.parent().text()

			if text in self.EDITORS:
				editor = self.EDITORS[text](self, item.data())
				editor.qtitem = item
				self.change_editor(editor)
			else:
				print("No editor found for", text)
				