import sys
import os
import platform

if sys.platform == 'win32':
	if os.environ["PROCESSOR_ARCHITECTURE"] == "AMD64":
		from .enet_win64 import *
	else:
		from .enet_win32 import *
elif sys.platform == 'linux2':
	if platform.architecture()[0] == '64bit':
		from .enet_linux2_64 import *
	else:
		from .enet_linux2_32 import *
else:
	raise ImportError("Unsupported platform:", sys.platform)
