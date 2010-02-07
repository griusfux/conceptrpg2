from lxml import etree

class PlayerClass:
	"""A container for data from classfiles"""
	
	def __init__(self, classfile):
		# First initialize all vars to 0/empty strings
		# We probably don't need these inited since the xml file is
		# Required to have the tags
		# self.KeyAbilities = ""
		# self.Role = ""
		# self.Proficiencies = 0
		
		# self.HPFirstLevel = 0
		# self.HPPerLevel = 0
		
		# self.FortAdj = 0
		# self.ReflexAdj = 0
		# self.WillAdj = 0
		
		# self.HealingSurges = 0
		
		# Now iterate the xml datag
		for element in classfile.Root.iter():
			if element.tag == "key_abilities":
				self.KeyAbilities = element.text
			elif element.tag == "role":
				self.Role = element.text
			elif element.tag == "proficiencies":
				self.Proficiencies = element.text
			elif element.tag == "hp_first_level":
				self.HPFirstLevel = element.text
			elif element.tag == "hp_per_level":
				self.HPPerLevel = element.text
			elif element.tag == "fort_adj":
				self.fort_adj = element.text
			elif element.tag == "reflex_adj":
				self.reflex_adj = element.text
			elif element.tag == "will_adj":
				self.will_adj = element.text
			elif element.tag == "healing_surges":
				self.HealingSurges = element.text