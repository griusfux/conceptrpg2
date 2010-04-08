import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Scripts.ClassData import ClassData
from Scripts.MapData import MapData
from Scripts.MonsterData import MonsterData
from Scripts.ItemData import *
from Scripts.ArchiveFile import *

from EditorFiles.EmptyEditor import *
	
class MainWidget(QWidget):
	def __init__(self, parent):
		QWidget.__init__(self, parent)
		
		splitter = QSplitter(self)
		splitter.childrenCollapsible = False
		splitter.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
				
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
		# self.create_subtree('Races', RaceFile, RaceData)
		self.create_subtree('Shields', ShieldFile, ShieldData)
		self.create_subtree('Weapons', WeaponFile, WeaponData)
		
		left = QTreeView()
		left.setHeaderHidden(True)
		left.setModel(model)
		splitter.addWidget(left)
		
		right = EmptyEditor(self)
		splitter.addWidget(right)
		splitter.
		
		hbox = QHBoxLayout()
		hbox.addWidget(splitter)
		# hbox.addWidget(left, 1)
		# hbox.addWidget(right, 4)
		
		self.setLayout(hbox)
		
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