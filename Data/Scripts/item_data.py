from Scripts.validate_data import *

class ArmorData():
	"""A data object to handle armor"""
	
	def __init__(self, datafile):
		self.allowed_types = ('none', 'light', 'heavy')
		self.name		= ""
		self.weight		= 0
		self.value		= 0
		
		self.type		= ""
		self.ac_bonus	= 0
		self.speed		= 0
		self.valid = True
		
		print("Loading %s . . ." % datafile.file_name)
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "value":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "type":
				ValidateAllowedData(self, element.tag, element.text, self.allowed_types)
			elif element.tag == "ac_bonus":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "speed":
				ValidateInt(self, element.tag, element.text)

class ShieldData():
	"""A data object to handle shields"""
	def __init__(self, datafile):
		self.allowed_types = ('none', 'light', 'heavy')
		self.name		= ""
		self.weight		= 0
		self.value		= 0
		self.type		= ""
		
		self.shield_bonus	= 0
		
		print("Loading %s . . ." % datafile.file_name)
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "value":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "type":
				ValidateAllowedData(self, element.tag, element.text, self.allowed_types)
			elif element.tag == "shield_bonus":
				ValidateInt(self, element.tag, element.text)
				
class WeaponData():
	"""A data object to handle Weapons"""
	def __init__(self, datafile):
		self.allowed_groups = ('axe', 'bow', 'crossbow', 'flail', 'hammer', 'heave blade', 'light blade', 'mace', 'pick', 'axe-polearm', 'sling', 'spear', 'staff', 'unarmed')
		self.allowed_categories = ('simple', 'martial', 'superior', 'improvised')
		self.allowed_properties = ('heavy thrown', 'high crit', 'light thrown', 'off-hand', 'reach', 'small', 'versatile', 'none')
		self.valid = True
		
		self.name	= ""
		self.weight	= 0
		self.value	= 0
		self.group	= ""
		self.category = ""
		
		self.two_hand	= False
		self.ranged		= False
		
		self.profeciency = 0
		self.damage	= "0d0"
		self.range	= "0/0"
		self.properties	= []
		
		print("Loading %s . . ." % datafile.file_name)
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "value":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "group":
				ValidateAllowedData(self, element.tag, element.text, self.allowed_groups)
			elif element.tag == "category":
				ValidateAllowedData(self, element.tag, element.text, self.allowed_categories)
			elif element.tag == "two_hand":
				ValidateBoolean(self, element.tag, element.text)
			elif element.tag == "ranged":
				ValidateBoolean(self, element.tag, element.text)
			elif element.tag == "profeciency":
				ValidateInt(self, element.tag, element.text)
			elif element.tag == "damage":
				ValidateSplit(self, element.tag, element.text, 'd')
			elif element.tag == "range":
				ValidateSplit(self, element.tag, element.text, '/')					
			elif element.tag == "properties":
				ValidateList(self, element.tag, element.text, self.allowed_properties)
				