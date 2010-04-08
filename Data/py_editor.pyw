import sys
from PyQt4.QtGui import *
from EditorFiles.EditorWindow import EditorWindow

app = QApplication(sys.argv)
window = EditorWindow()
window.show()

sys.exit(app.exec_())