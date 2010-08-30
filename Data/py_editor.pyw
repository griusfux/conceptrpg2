import sys
import os
from PyQt4.QtGui import *
from EditorFiles.EditorWindow import EditorWindow

# Windows 7 hack
if os.name == 'nt':
	import ctypes
	myappid = 'crpg2.editor' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon('icon.png'))
window = EditorWindow()
window.show()

sys.exit(app.exec_())