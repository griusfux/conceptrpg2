from PyQt4.QtGui import *
import sys

class Logger:
	def __init__(self, edit, out=None, color=None):
		self.edit = edit
		self.out = out
		self.color = color
		
	def write(self, msg):
		if self.color:
			old_col = self.edit.textColor()
			self.edit.setTextColor(self.color)
			
		self.edit.moveCursor(QTextCursor.End)
		self.edit.insertPlainText(msg)
		
		if self.color:
			self.edit.setTextColor(old_col)
			
		if self.out:
			self.out.write(msg)
			
class LogWidget(QTextEdit):
	def __init__(self, parent=None):
		QTextEdit.__init__(self, parent)
		
		self.setReadOnly(True)
		
		self.stdout = Logger(self, sys.stdout)
		self.stderr = Logger(self, sys.stderr, QColor(255, 0, 0))
		
		
		
		sys.stdout = self.stdout
		sys.stderr = self.stderr