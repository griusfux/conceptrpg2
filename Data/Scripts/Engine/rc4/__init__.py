try:
	from ._rc4 import *
except ImportError:
	from .rc4 import *