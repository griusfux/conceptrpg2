import sys
import os

# This allows the editor to find the necessary libs when in a "release" configuration
# sys.path.append(os.path.join(os.getcwd(), '2.58', 'python', 'lib', 'site-packages'))
sys.path.append("extern")

from PySide.QtGui import *
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