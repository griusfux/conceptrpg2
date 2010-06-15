from Scripts.validate_data import *

class PowerData():
	"""A data object to handle powers"""
	
	def __init__(self, datafile):
		
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text