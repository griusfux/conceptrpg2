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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from ..common import edit_text_file

class BaseEditor(QFrame):
    def __init__(self, parent, data, ui):
        QFrame.__init__(self, parent)
        
        self.data = data
        
        # Create the ui
        self.ui = ui()
        self.ui.setupUi(self)
        
        # Setup an image if we have one
        if hasattr(self.ui, "data_image"):
            image = QPixmap(data.open_image())
            data.close_image()
            self.ui.data_image.setPixmap(image)
        
    def save(self):
        raise NotImplementedError("save")
    
    def modified(self):
        if hasattr(self, "qtitem"):
            self.save()
            self.qtitem.setForeground(Qt.red)
            
    def edit_text(self):
    	if hasattr(self, "pyfile"):
    		edit_text_file(os.path.join(self.data._dir, self.data.package_name, self.pyfile))