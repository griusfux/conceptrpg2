# This is a wrapper script for mathutils. The wrapper is to keep the server
# from choking when trying to import this through states

try:
	from mathutils import *
except ImportError:
	Vector = None
	Matrix = None
