import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Scripts.packages import *

from EditorFiles.LogWidget import *
from EditorFiles.Editors import *

EDITORS = {
	'Armors': ArmorEditor,
	'Items': ItemEditor,
	'Maps': MapEditor,
	'Monsters': MonsterEditor,
	'Weapons': WeaponEditor,
	}

class EditorWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Window
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('Editor')
		
		# Logger
		logger = LogWidget(self)
		
		# Menu
		save = QAction('&Save', self)
		save.setShortcut('Ctrl+S')
		save.setStatusTip('Save the currently selected package')
		self.connect(save, SIGNAL('triggered()'), self.save_file)
		
		exit = QAction('E&xit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit the application')
		self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))
		
		file = self.menuBar().addMenu('&File')
		file.addAction(save)
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
		# self.create_subtree('Classes', Class)
		self.create_subtree('Decks', EncounterDeck)
		self.create_subtree('Items', Item)
		self.create_subtree('Maps', Map)
		self.create_subtree('Monsters', Monster)
		self.create_subtree('Powers', Power)
		self.create_subtree('Races', Race)
		# self.create_subtree('Shields', Shield)
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
		
	def save_file(self):
		if hasattr(self.editor, "data"):
			print("Saving %s..." % self.editor.data.name)
			self.editor.save()
			self.editor.data.write()
		
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
				print(e)
				print('Unable to open', file)
				continue

			item =  QStandardItem(arc_file.name)
			item.setEditable(False)
			sub_root.appendRow(item)
			self.data_files[type][arc_file.name] = arc_file
			
	def change_editor(self, editor):
		# Save changes so they can be restored
		if hasattr(self.editor, "save"):
			self.editor.save()
		
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

			if text in EDITORS:
				self.change_editor(EDITORS[text](self, self.data_files[text][item.text()]))
			else:
				print("No editor found for", text)
				