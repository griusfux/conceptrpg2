from PyQt4.QtGui import *
from PyQt4.QtCore import *

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