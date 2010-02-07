class ArmorData():
	"""A data object to handle armor"""
	
	def __init__(self, datafile):
		self.name		= ""
		self.weight		= 0
		self.value		= 0
		
		self.type		= 0
		self.ac_bonus	= 0
		self.speed		= 0
		
		for element in datafile.Root.iter():
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				self.weight = int(element.text)
			elif element.tag == "value":
				self.value = int(element.text)
			elif element.tag == "type":
				self.type = element.text
			elif element.tag == "ac_bonus":
				self.ac_bonus = int(element.text)
			elif element.tag == "speed":
				self.speed = int(element.text)

class ShieldData():
	"""A data object to handle shields"""
	def __init__(self):
		self.name		= ""
		self.weight		= 0
		self.value		= 0
		
		self.shield_bonus	= 0
		
		for element in datafile.Root.iter():
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				self.weight = element.text
			elif element.tag == "value":
				self.value = element.text
			elif element.tag == "shield_bonus":
				self.shield_bonus = int(element.text)