from Scripts.validate_data import *
import sys

class PowerData():
	"""A data object to handle powers"""
	
	def __init__(self, datafile):
	
		# Get the power function
		location = datafile.origin
		
		if datafile.is_zip:
			location += "."+datafile._ext
			
		sys.path.append(location)
		import power
		
		self.method = power.power
		
		sys.path.remove(location)
		
		# Parse the tags
		
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "animation":
				self.animation = element.text