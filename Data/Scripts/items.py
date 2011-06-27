import random

import Scripts.packages as Packages

AvailableItems = [i.name for i in Packages.Item.get_package_list()]
AvailableArmors = [i.name for i in Packages.Armor.get_package_list()]
AvailableWeapons = [i.name for i in Packages.Weapon.get_package_list()]

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
	Translate = {
				"cost" : lambda x: x,
				}
	
	def __init__(self, base):
		self._base = base
		self._datafile = getattr(Packages, self.__class__.__name__)(base)
		self.name = self._datafile.name
		self._cost = self._datafile.cost
		self._modified = self
		
	def createObjectInstance(self, engine, position=(0,0,0), orientation=(0,0,0),time=0):
		if not self._datafile.blend:
			return None
		
		engine.load_library(self._datafile)
		obj = engine.add_object(self._datafile.name, position, orientation, time)
		return obj
			
	@property
	def cost(self):
		return Item.Translate['cost'](self._modified._cost)
		
class Armor(Item):
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
		Item.__init__(self, base)
		self.name = TierNames[tier] + " " + self.name
		self.type = self._datafile.type
		self._arcane_defense = self._datafile.arcane_defense
		self._physical_defense = self._datafile.physical_defense
		self._reflex = self._datafile.reflex
		
		for i in range(max(0, random.randint(2, 4) + tier - 4)):
			modified = False
			while not modified:
				modified = self.modify(random.choice(ArmorModifiers), tier)
		
	def modify(self, name, value):
		try:
			modified = globals()['_'+name](self._modified, value)
		except KeyError:
			print("No modifier of the name %s exists" % name)
			return False
		if not isinstance(modified, Armor):
			print("%s is not an armor modifier" % name)
			return False
		else:
			self._modified = modified
			
		return True
	
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
						"range" : lambda x: x,
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
		Item.__init__(self, base)
		self.name = TierNames[tier] + " " + self.name
		self.type = self._datafile.type
		self.hands = self._datafile.hands
		self._weight = self._datafile.weight
		self._range = self._datafile.range
		self._accuracy = self._datafile.accuracy
		
		for i in range(max(0, random.randint(2, 4) + tier - 5)):
			modified = False
			while not modified:
				modified = self.modify(random.choice(WeaponModifiers), tier)
		
	def modify(self, name, value):
		try:
			modified = globals()['_'+name](self._modified, value)
		except KeyError:
			print("No modifier of the name %s exists" % name)
			return False
		if not isinstance(modified, Weapon):
			print("%s is not a weapon modifier" % name)
			return False
		else:
			self._modified = modified
			
		return True
	
	@property
	def range(self):
		return Weapon.Translate[self.type]['range'](self._modified._range)
	
	@property
	def accuracy(self):
		return Weapon.Translate[self.type]['accuracy'](self._modified._accuracy)
	
class _ArmorModifier(Armor):
	def __init__(self, armor, value):
		self._armor = armor
		self.value = value
		self.type = armor.type
		
	@property
	def name(self):
		return self._armor.name
	
	@property
	def _arcane_defense(self):
		return self._armor._arcane_defense
	
	@property
	def _physical_defense(self):
		return self._armor._physical_defense
	
	@property
	def _reflex(self):
		return self._armor._reflex

class _arcane_defense(_ArmorModifier):
	@property
	def _arcane_defense(self):
		return self._armor._arcane_defense + self.value
	
class _WeaponModifier(Weapon):
	def __init__(self, weapon, value):
		self._weapon = weapon
		self.value = value
		self.type = weapon.type
		
	@property
	def name(self):
		return self._weapon.name
		
	@property
	def _range(self):
		return self._weapon._range
	
	@property
	def _accuracy(self):
		return self._weapon._accuracy
	
	@property
	def _cost(self):
		return self._weapon._cost
	
class _accuracy(_WeaponModifier):
	@property
	def _accuracy(self):
		return self._weapon._accuracy + self.value