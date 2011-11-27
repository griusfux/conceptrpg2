import random

import Scripts.packages as Packages
from Scripts.modifiers import *

AvailableItems = [i.name for i in Packages.Item.get_package_list()]
AvailableArmors = [i.name for i in Packages.Armor.get_package_list()]
AvailableWeapons = [i.name for i in Packages.Weapon.get_package_list()]

MOD_LEVEL_MINUS_ONE = 0.2
MOD_LEVEL_PLUS_ONE = 0.4

ArmorModifiers =[
					"arcane_defense"
				]
WeaponModifiers = [
					"accuracy",	
					]

TierNames = {
			1 : "Flawed",
			2 : "",
			3 : "Tempered",
			4 : "Exceptional",
			5 : "Legendary"
			}

#print(AvailableItems)
#print(AvailableArmors)
#print(AvailableWeapons)

class Item:
	available_items = AvailableItems
	
	Translate = {
				"cost" : lambda x: x,
				}
	
	def __init__(self, base, tier):
		self._base = base
		self.tier = tier
		self._datafile = getattr(Packages, self.__class__.__name__)(base)
		self.name = self._datafile.name
		self.name = TierNames[tier] + " " + self.name if TierNames[tier] else self.name
		self.description = self._datafile.description
		self._cost = self._datafile.cost
		self._modified = self
		
	def __str__(self):
		retval = self.name
		for i in self.modifiers:
			retval += "\n\t"+i
			
		return retval
		
	def modify(self, name, value):
		# We want to randomize modifier levels a bit
		r = random.random()
		if r < MOD_LEVEL_MINUS_ONE:
			value -= 1
		elif r < MOD_LEVEL_PLUS_ONE:
			value += 1
		
		# We don't want to go above Legendary
		if value > 5:
			value = 5
		try:
			modified = globals()[name](self._modified, value)

		except KeyError:
			print("No modifier of the name %s exists" % name)
			return False
		if modified.mod_type != self.__class__.__name__:
			print(modified.type)
			print("%s is not a %s modifier" % (name, self.__class__.__name__))
			return False
		else:
			self._modified = modified
			
		return True
		
	def createObjectInstance(self, engine, position=None, orientation=None,time=0):
		if not self._datafile.blend:
			return None
		
		engine.load_library(self._datafile)
		obj = engine.add_object(self._datafile.name, position, orientation, time)
		return obj
			
	@property
	def cost(self):
		return Item.Translate['cost'](self._modified._cost)
	
	@property
	def _modifiers(self):
		return []
	
	@property
	def modifiers(self):
		return self._modified._modifiers
		
class Armor(Item):
	available_items = AvailableArmors
	
	Translate = {}
	Translate['METAL'] = {
						"arcane_defense" : lambda x: x,
						"physical_defense" : lambda x: x,
						"reflex" : lambda x: x,
						}
	Translate['CLOTH'] = {
						"arcane_defense" : lambda x: x,
						"physical_defense" : lambda x: x,
						"reflex" : lambda x: x,
						}
	Translate['LEATHER'] = {
						"arcane_defense" : lambda x: x,
						"physical_defense" : lambda x: x,
						"reflex" : lambda x: x,
						}
						
	for key in Translate:
		Translate[key].update(Item.Translate)
						
	def __init__(self, base, tier=1):
		Item.__init__(self, base, tier)
		self.type = self._datafile.type
		self._arcane_defense = self._datafile.arcane_defense
		self._physical_defense = self._datafile.physical_defense
		self._reflex = self._datafile.reflex
		
		for i in range(max(0, random.randint(2, 4) + tier - 4)):
			modified = False
			while not modified:
				modified = self.modify(random.choice(ArmorModifiers), tier)

	@property
	def arcane_defense(self):
		return Armor.Translate[self.type]['arcane_defense'](self._modified._arcane_defense)
		
	@property
	def physical_defense(self):
		return Armor.Translate[self.type]['physical_defense'](self._modified._physical_defense)
		
	@property
	def reflex(self):
		return Armor.Translate[self.type]['reflex'](self._reflex)

class Weapon(Item):
	available_items = AvailableWeapons
	
	Translate = {}
	Translate['SWORD'] = {
						"weight" : lambda x: x,
						"range" : lambda x: max(0.25, 1 + (0.25*x)),
						"accuracy" : lambda x: x,
						}
	
	Translate['AXE'] = {
						"weight" : lambda x: x,
						"range" : lambda x: max(0.25, 1 + (0.25*x)),
						"accuracy" : lambda x: x,
						}
	
	Translate['POLEARM'] = {
						"weight" : lambda x: x,
						"range" : lambda x: max(0.5, 2 + (0.5*x)),
						"accuracy" : lambda x: x,
						}
	
	Translate['BLUNT'] = {
						"weight" : lambda x: x,
						"range" : lambda x: max(0.25, 1 + (0.25*x)),
						"accuracy" : lambda x: x,
						}
	
	Translate['BOW'] = {
						"weight" : lambda x: x,
						"range" : lambda x: max(5, 10 + 5*x),
						"accuracy" : lambda x: x,
						}
	
	Translate['GUN'] = {
						"weight" : lambda x: x,
						"range" : lambda x: x,
						"accuracy" : lambda x: x,
						}
	
	Translate['THROWN'] = {
						"weight" : lambda x: x,
						"range" : lambda x: x,
						"accuracy" : lambda x: x,
						}
						
	for key in Translate:
		Translate[key].update(Item.Translate)
		
	def __init__(self, base, tier=1):
		Item.__init__(self, base, tier)
		self.type = self._datafile.type
		self.hands = self._datafile.hands
		self._weight = self._datafile.weight
		self._range = self._datafile.range
		self._accuracy = self._datafile.accuracy
		
		for i in range(max(0, random.randint(2, 4) + tier - 5)):
			modified = False
			while not modified:
				modified = self.modify(random.choice(WeaponModifiers), tier)
	
	@property
	def range(self):
		return Weapon.Translate[self.type]['range'](self._modified._range)
	
	@property
	def accuracy(self):
		return Weapon.Translate[self.type]['accuracy'](self._modified._accuracy)
	
	@property
	def damage(self):
		return 5
