import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Scripts.class_data import ClassData
from Scripts.map_data import MapData
from Scripts.monster_data import MonsterData
from Scripts.race_data import RaceData
from Scripts.item_data import *
from Scripts.archive_file import *

from EditorFiles.LogWidget import *
from EditorFiles.Editors import *

class EditorWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Window
		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('Editor')
		
		# Logger
		logger = LogWidget(self)
		
		# Menu
		exit = QAction(QIcon('icon.png'), 'E&xit', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit the application')
		self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))
		
		file = self.menuBar().addMenu('&File')
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
		self.create_subtree('Armor', ArmorFile, ArmorData)
		self.create_subtree('Classes', ClassFile, ClassData)
		# self.create_subtree('Decks', DeckFile, DeckData)
		self.create_subtree('Maps', MapFile, MapData)
		self.create_subtree('Monsters', MonsterFile, MonsterData)
		self.create_subtree('Races', RaceFile, RaceData)
		self.create_subtree('Shields', ShieldFile, ShieldData)
		self.create_subtree('Weapons', WeaponFile, WeaponData)
		
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
		
	def create_subtree(self, type, Archive, DataFile):
		sub_root = QStandardItem(type)
		self.data_files[type] = {}
		self.root.appendRow(sub_root)
		
		# Build a list of the files to use
		files = [i.split('.')[0] for i in os.listdir(Archive._dir) if not i.startswith('.')]
		
		# Remove duplicates
		for file in files:
			while files.count(file) > 1:
				files.remove(file)
		
		# Load the files
		for file in files:
			if file.startswith('.'): continue
			arc_file = Archive(file)
			
			if not arc_file.init:
				arc_file.close()
				print('Error with: ' + file)
				continue
				
			d_file = DataFile(arc_file)
			arc_file.close()
			
			item =  QStandardItem(d_file.name)
			sub_root.appendRow(item)
			self.data_files[type][d_file.name] = d_file
			
	def change_editor(self, editor):
		self.right.widget(0).hide()
		self.right.widget(0).deleteLater()
		self.right.insertWidget(0, editor)
		self.right.setStretchFactor(0, 40)
		self.right.setStretchFactor(1, 1)
		
			
	def tree_clicked(self, index):
		item = self.model.itemFromIndex(index)
		
		if item.parent():
			text = item.parent().text()

			if text == 'Monsters':
				self.change_editor(MonsterEditor(self, QImage('icon.png'), self.data_files['Monsters'][item.text()]))
				