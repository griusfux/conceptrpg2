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
import Scripts.packages as p

from .NewDialog_ui import Ui_NewDialog

TYPES = [
	'Armor',
	'Item',
	'Map',
	'Monster',
	'Power',
	'Status',
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
			if package_type[-1] == 's':
				package_type += 'es'
			else:
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
