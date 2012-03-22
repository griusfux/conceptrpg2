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

from .SettingsDialog_ui import Ui_SettingsDialog
from .common import SETTINGS

import os

class SettingsDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        
        self.editor = parent
        
        # Create the ui
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        
        self.ui.blender_path.setText(SETTINGS['blender_path'])
        self.ui.text_editor_path.setText(SETTINGS['text_editor_path'])
        
        
    def accept(self):
        SETTINGS['blender_path'] = self.ui.blender_path.text()
        SETTINGS['text_editor_path'] = self.ui.text_editor_path.text()
        self.close()
    
    def find_blender(self):
        path = QFileDialog.getOpenFileName(parent=self,
                                           caption='Select a Blender binary',
                                           directory=os.path.dirname(self.ui.blender_path.text()))[0]

        self.ui.blender_path.setText(os.path.abspath(path))
        
    def find_text_editor(self):
    	path = QFileDialog.getOpenFileName(parent=self,
										caption='Select a text editor',
										directory=os.path.dirname(self.ui.text_editor_path.text()))[0]
    	
    	self.ui.text_editor_path.setText(os.path.abspath(path))