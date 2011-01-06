import sys
import os

if sys.platform == 'win32':
	if os.environ["PROCESSOR_ARCHITECTURE"] == "AMD64":
		from .enet_win64 import *
	else:
		from .enet_win32 import *
