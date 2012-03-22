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