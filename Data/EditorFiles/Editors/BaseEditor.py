from PyQt4.QtGui import *
from PyQt4.QtCore import *

class BaseEditor(QFrame):
    def __init__(self, parent, data, ui):
        QFrame.__init__(self, parent)
        
        self.data = data
        
        # Create the ui
        self.ui = ui()
        self.ui.setupUi(self)
        
    def save(self):
        raise NotImplementedError("save")
    
    def modified(self):
        if hasattr(self, "qtitem"):
            self.save()
            self.qtitem.setForeground(Qt.red)