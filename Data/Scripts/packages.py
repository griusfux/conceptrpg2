from .Engine.packages import *
import imp

class Map(Package):
	"""Map package"""
	
	_ext = 'map'
	_blend = 'map.blend'
	_config = 'map.json'
	_schema = 'Schemas/mapfile.json'
	_dir = 'Maps'
	
class EncounterDeck(Package):
	"""Encounter deck package"""
	
	def __init__(self, package_name, new_package=False):
		Package.__init__(self, package_name, new_package)
		
		# Build a deck
		self._cards = self.cards[:]
		
		self.cards = []
		for card in self._cards:
			self.cards.extend([card for i in range(card['weight'])])
	
	_ext = 'deck'
	_blend = ''
	_config = 'deck.json'
	_schema = 'Schemas/deckfile.json'
	_dir = 'EncounterDecks'
	
class Monster(Package):
	"""Monster package"""
	
	_ext = 'monster'
	_blend = 'monster.blend'
	_config = 'monster.json'
	_schema = 'Schemas/monsterfile.json'
	_dir = 'Monsters'
	_img = 'monster.png'
	
class Race(Package):
	"""Race package"""
	
	_ext = 'race'
	_blend = 'race.blend'
	_config = 'race.json'
	_schema = 'Schemas/racefile.json'
	_dir = 'Races'
	_img = 'race.png'
	
class Class(Package):
	"""Player class package"""
	
	_ext = 'class'
	_config = 'class.json'
	_schema = 'Schemas/classfile.json'
	_dir = 'Classes'
	_img = 'class.png'

class Power(Package):
	"""Power package"""
	
	_ext = 'power'
	_blend = ''
	_config = 'power.json'
	_schema = 'Schemas/powerfile.json'
	_dir = 'Powers/Powers'
	_img = 'power.png'
	
	def __init__(self, package_name, new_package=False):
		Package.__init__(self, package_name, new_package)
		
		# Create a script file if this is a new package
		if new_package:
			open(os.path.join(self._dir, package_name, 'power.py'), 'wb').close()

		# Load power.py as a module
		self._module = imp.new_module(package_name)
		exec(self._package.read("power.py"), self._module.__dict__)
		
		# Set up a timer to use for cooldowns
		self.timer = 0
		
	def use(self, controller, user):
		mod = self._module
		if hasattr(mod, "power"):
			mod.power(self, controller, user)
		else:
			pass
		
	def push(self, controller, user):
		mod = self._module
		if hasattr(mod, "push"):
			mod.push(self, controller, user)
		else:
			pass
			
	def pop(self, controller, user):
		mod = self._module
		if hasattr(mod, "pop"):
			mod.pop(self, controller, user)
		else:
			pass
	
	def write(self):
		Package.write(self)
		
		   
		
	def pack(self, path):
		Package.pack(self, path)
		
		zip = zipfile.ZipFile(path+'.'+self._ext, "a", zipfile.ZIP_DEFLATED)
		
		# Copy py file
		zip.write(os.path.join(self._path, 'power.py'), arcname='power.py')
		
		zip.close()
		
	def cost(self, affinities):
		if self.tier == 0:
			return 0
		
		tier = min(self.tier, 5)
		
		cost = [3, 8, 15, 24, 35][tier-1]
		cost -= affinities[self.element.upper()] + affinities[self.delivery.upper()]
		
		return max(1, cost)
		
class Feat(Power):
	_dir = 'Powers/Feats'
	_schema = 'Schemas/featfile.json'
	
class Status(Power):
	_dir = 'Powers/Statuses'
	_schema = 'Schemas/statusfile.json'
	
	def __init__(self, package_name, new_package=False):
		Power.__init__(self, package_name, new_package)
		self.amount = 0
	
		
class Item(Package):
	"""Item Package"""
	
	_ext = 'item'
	_config = 'item.json'
	_schema = 'Schemas/itemfile.json'
	_new = 'Schemas/itemfile_new.json'
	_dir = 'Items/Others'
	_img = 'item.png'
	
class Weapon(Item):
	"""Weapon Package"""
	
	_config = 'weapon.json'
	_blend = 'weapon.blend'
	_parent_schema = Item._schema
	_schema = 'Schemas/weaponfile.json'
	_dir = 'Items/Weapons'
	_img = 'weapon.png'
	
class Armor(Item):
	"""Armor Package"""
	
	_config = 'armor.json'
	_parent_schema = Item._schema
	_schema = 'Schemas/armorfile.json'
	_dir = 'Items/Armors'
	_img = 'armor.png'
	
class ActionSet(Package):
	"""Action Set Package"""
	
	_ext = 'as'
	_blend = 'actionset.blend'
	_config = 'actionset.json'
	_schema = 'Schemas/actionsetfile.json'
	_new = 'Schemas/actionsetfile_new.json'
	_dir = 'ActionSets'
	
	def __init__(self, package_name, new_package=False):
		Package.__init__(self, package_name, new_package)
		
		self.actions = {}
		
		for action in self.action_set:
			self.actions[action['name']] = action['actions']
	
class Shop(Package):
	"""Shop package"""
	
	_ext = 'shop'
	_blend = 'shop.blend'
	_config = 'shop.json'
	_schema = 'Schemas/shopfile.json'
	_new = 'Schemas/shopfile_new.json'
	_dir = 'Shops'
	
	def __init__(self, package_name, new_package=False):
		Package.__init__(self, package_name, new_package)
		
		# Build item lists
		self.items = []
		self.weapons = []
		self.armors = []
		
		for f in os.listdir(os.path.join('Shops', '.config')):
			if f.lower().startswith(package_name.lower()):
				self._parse_conf(os.path.join('Shops', '.config', f))
					
	def _parse_conf(self, path):
		curr_list = self.items
		curr_package = Item
	
		with open(path) as conf:
			for line in conf.readlines():
				line = line.strip()
				
				if not line:
					continue
				elif line == "[Items]":
					curr_list = self.items
					curr_package = Item
				elif line == "[Weapons]":
					curr_list = self.weapons
					curr_package = Weapon
				elif line == "[Armors]":
					curr_list = self.armors
					curr_package = Armor
				else:
					try:
						curr_list.append(curr_package(line))
					except Exception as e:
						print(e)
						print("Failed to load package:", line)
						
class Save(Package):
	"""Save package"""
	
	_ext = 'save'
	_config = 'save.json'
	_schema = 'Schemas/savefile.json'
	_new = 'Schemas/savefile_new.json'
	_dir = '../Saves'
	_img = 'save.png'
	
	def __init__(self, package_name, new_package=False):
		Package.__init__(self, package_name, new_package)
		
		# Load up the data file
		try:
			self.data = pickle.loads(self._package.read("data"))
		except IOError:
			self.data = {}
		
	def pack(self, path):
		Package.pack(self, path)
		
		zip = zipfile.ZipFile(path+'.'+self._ext, "a", zipfile.ZIP_DEFLATED)
		
		# Copy data file
		zip.write(os.path.join(self._path, 'data'), arcname='data')
		
		zip.close()
		
	def write(self):
		Package.write(self)
	
		with open(os.path.join(self._path, 'data'), 'wb') as f:
			pickle.dump(self.data, f)
			
class Effect(Package):
	"""Effect Package"""
	
	_ext = 'fx'
	_blend = 'effect.blend'
	_config = 'effect.json'
	_schema = 'Schemas/effect.json'
	_new = 'Schemas/effect_new.json'
	_dir = 'Effects'