class ClassData:
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
		for element in classfile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "key_abilities":
				self.key_abilities = element.text
			elif element.tag == "role":
				self.role = element.text
			elif element.tag == "proficiencies":
				self.proficiencies = element.text
			elif element.tag == "hp_first_level":
				self.hp_first_level = int(element.text)
			elif element.tag == "hp_per_level":
				self.hp_per_level = int(element.text)
			elif element.tag == "fort_adj":
				self.fort_adj = int(element.text)
			elif element.tag == "reflex_adj":
				self.reflex_adj = int(element.text)
			elif element.tag == "will_adj":
				self.will_adj = int(element.text)
			elif element.tag == "healing_surges":
				self.healing_surges = int(element.text)