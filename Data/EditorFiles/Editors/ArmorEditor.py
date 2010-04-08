from PyQt4.QtGui import *

class ArmorEditor(QWidget):
	def __init__(self, parent, data):
		QWidget.__init__(self, parent)
		
		self.data = data