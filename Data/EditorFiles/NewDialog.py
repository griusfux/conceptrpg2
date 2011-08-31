from PyQt4.QtGui import *
import Scripts.packages as p

from .NewDialog_ui import Ui_NewDialog

TYPES = [
	'Armor',
	'Item',
	'Map',
	'Monster',
	'Power',
	'Weapon'
]

class NewDialog(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		
		self.editor = parent
		
		# Create the ui
		self.ui = Ui_NewDialog()
		self.ui.setupUi(self)
		
		self.ui.package_name.setText("NewPackage")
		self.ui.package_type.addItems(TYPES)
		
		
	def accept(self):
		package_type = self.ui.package_type.itemText(self.ui.package_type.currentIndex())
		package_name = self.ui.package_name.text()
		package = getattr(p, package_type).create(package_name)
		package.name = package_name
		
		if package:
			# Unlike the package system, the editor uses the plural forms of the 
			# package types, so change to plural for this part
			package_type += 's'
		
			# Add the new package to the data_files
			self.editor.data_files[package_type][package_name] = package
			
			# Find the appropriate spot in the tree to add the package
			for i in range(self.editor.root.rowCount()):
				child = self.editor.root.child(i, 0)
				if child.text() == package_type:
					item = QStandardItem(package_name)
					item.setData(package)
					item.setEditable(False)
					child.appendRow(item)
					child.sortChildren(0)
					
			# Now switch to the new file
			self.editor.change_editor(self.editor.EDITORS[package_type](self.editor, package))
			self.close()
		else:
			msg = QMessageBox();
			msg.setText("Failed to create the package!\nCheck to see if the package has already been created.")
			msg.exec()
