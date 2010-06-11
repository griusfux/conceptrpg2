from Scripts.validate_data import *

class RaceData:
	"""A container for data from racefiles"""
	
	def __init__(self, datafile):
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			if element.tag == "root_object":
				self.root_object = element.text