from PyQt4.QtGui import *

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
        
        
    def accept(self):
        SETTINGS['blender_path'] = self.ui.blender_path.text()
        self.close()
    
    def find_file(self):
        path = QFileDialog.getOpenFileName(parent=self,
                                           caption='Select a Blender binary',
                                           directory=os.path.dirname(self.ui.blender_path.text()))
        
        self.ui.blender_path.setText(os.path.abspath(path))