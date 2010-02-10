class ArmorData():
	"""A data object to handle armor"""
	
	def __init__(self, datafile):
		self.allowed_types = ('none', 'light', 'heavy')
		# self.name		= ""
		# self.weight		= 0
		# self.value		= 0
		
		# self.type		= 0
		# self.ac_bonus	= 0
		# self.speed		= 0
		self.valid = True
		
		print("Loading %s . . ." % datafile.file_name)
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				try:
					self.weight = int(element.text)
				except ValueError:
					print("Unable to get an int from the weight tag")
					self.valid = False
			elif element.tag == "value":
				try:
					self.value = int(element.text)
				except ValueError:
					print("Unable to get an int from the value tag")
					self.valid = False
			elif element.tag == "type":
				if element.text.lower() in self.allowed_types:
					self.type = element.text
				else:
					printf("%s in type tag is not a valid category.\nThe valid categories are %s", element.text, allowed_types)
					self.valid = False
			elif element.tag == "ac_bonus":
				try:
					self.ac_bonus = int(element.text)
				except ValueError:
					print("Unable to get an int from the ac_bonus tag")
					self.valid = False
			elif element.tag == "speed":
				try:
					self.speed = int(element.text)
				except ValueError:
					print("Unable to get an int from the speed tag")
					self.valid = False

class ShieldData():
	"""A data object to handle shields"""
	def __init__(self):
		# self.name		= ""
		# self.weight		= 0
		# self.value		= 0
		
		# self.shield_bonus	= 0
		
		for element in datafile.root:
			if element.tag == "name":
				self.name = element.text
			elif element.tag == "weight":
				self.weight = element.text
			elif element.tag == "value":
				self.value = element.text
			elif element.tag == "shield_bonus":
				self.shield_bonus = int(element.text)
				
# class WeaponData():
	# """A data object to handle Weapons"""
	# def __init__(self):
		# allowed_groups = ('axe', 'bow', 'crossbow', 'flail', 'hammer', 'heave blade', 'light blade', 'mace', 'pick', 'axe-polearm', 'sling', 'spear', 'staff', 'unarmed')
		# allowed_categories = ('simple', 'martial', 'superior', 'improvised')
		# allowed_properties = ('heavy thrown', 'high crit', 'light thrown', 'off-hand', 'reach', 'small', 'versatile')
		# valid = True
		
		# self.name	= ""
		# self.weight	= 0
		# self.value	= 0
		# self.group	= ""
		# self.category = ""
		
		# self.two_hand	= False
		# self.ranged		= False
		
		# self.profeciency = 0
		# self.damage	= "0d0"
		# self.range	= "0/0"
		# self.properties	= []
		
		# for element in datafile.root:
			# if element.tag == "name":
				# self.name = element.text
			# elif element.tag == "weight":
				# try:
					# self.weight == int(element.text)
				# except ValueError:
					# print("Unable to get an int from the weight tag")
					# valid = False
			# elif element.tag == "value":
				# try:
					# self.value == int(element.text)
				# except ValueError:
					# print("Unable to get an int from the value tag")
					# valid = False
			# elif element.tag == "group":
				# if element.text in allowed_groups:
					# self.group = element.text
				# else:
					# printf("%s in group tag is not a valid group.\nThe valid groups are %s", element.text, allowed_groups)
					# valid = False
			# elif element.tag == "category":
				# if element.text in allowed_categories:
					# self.category = element.text
				# else:
					# printf("%s in category tag is not a valid category.\nThe valid categories are %s", element.text, allowed_categories)
					# valid = False
			# elif element.tag == "two_hand":
				# if element.text.lower() == "true":
					# self.two_hand = True
				# elif element.text.lower() == "false":
					# self.two_hand = False
				# else:
					# print("The two_hand tag does not contain true or false")
					# valid = False
			# elif element.tag == "ranged":
				# if element.text.lower() == "true":
					# self.ranged = True
				# elif element.text.lower() == "false":
					# self.ranged = False
				# else:
					# print("The ranged tag does not contain true or false")
					# valid = False
			# elif element.tag == "profeciency":
				# try:
					# self.profeciency = int(element.text)
				# except ValueError:
					# print("Unable to get an int from the profeciency tag")
					# valid = False
			# elif element.tag == "damage":
				# split = element.text.split('d')
				# if split == 2:
					# try:
						# x, y = [int(i) for i in split]
						# self.damage = element.text
					# except ValueError:
						# print("Invalid ints for die roll in damage tag.\nDice rolls should be in the format xdy, where x and y are integers")
						# valid = False
				# else:
					# print("Unable to parse die roll in damage tag. Make sure the values are seperate by a lowercase d")
					# valid = False
			# elif element.tag == "ranged":
				# split = element.text.split('/')
				# if split == 2:
					# try:
						# x, y = [int(i) for i in split]
						# self.range = element.text
					# except ValueError:
						# print("Invalid ints for range value in range tag.\nRange values should be in the format x/y, where x and y are integers")
						# valid = False
				# else:
					# print("Unable to parse range value in range tag. Make sure the values are seperate by a //")
					# valid = False
					
			# elif element.tag == "properties":
				# split = [i.lower() for i in element.text.split(', ')]
				# for property in split:
					# if property not in allowed_properties:
						# printf("%s is not a valid property", property)
						# valid = false
				# self.properties = split
				