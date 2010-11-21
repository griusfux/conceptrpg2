# $Id$

import json
import os
import imp
import shutil
import zipfile
import gzip
import io
import traceback
import tempfile

from . import rc4

class PackageError(Exception):
	"""Package file related errors"""
	pass
	
class PackageWarning(RuntimeWarning):
	"""Package file related warnings"""
	pass

class Directory:
	"""A class to make directories act a bit more like ZipFile"""
	
	def __init__(self, _dir):
		if not os.path.isdir(_dir):
			raise IOError(_dir+" was not a directory or didn't exist")
			
		self.dir = _dir
		
	def read(self, file):
		with open(self.dir+'/'+file, 'rb') as f:
			return f.read()
			

class Package:
	"""Base package class"""
	
	# Options for the package file
	_ext = 'zip'
	_blend = ''
	_config = ''
	_schema = ''
	_parent_schema = ''
	_new = ''
	_dir = ''
	_img = ''
	
	key = None
	
	def __init__(self, package_name):
		# Combine the package name and the directory to get the filepath
		path = self._dir + '/' + package_name
		
		# Check to see if the file is packed (unpacked takes precedence)
		if not os.path.exists(path):
			if os.path.exists(path+'.'+self._ext):
				path += '.'+self._ext
				if zipfile.is_zipfile(path):
					package = zipfile.ZipFile(path)
				elif self.key:
					# Assume the package is encrypted
					cipher = rc4.rc4(self.key, 0)
					with open(path, 'rb') as f:
						data = cipher.decode(f.read())
						
					package = zipfile.ZipFile(io.BytesIO(data))
			else:
				raise PackageError("Could not find package: "+package_name)
		else:
			package = Directory(path)
			
		# If there is a .blend file, load and store the data
		if self._blend:
			self.blend = package.read(self._blend)
			
			# Try to unpack the .blend if it's compressed
			try:
				with gzip.GzipFile(fileobj=io.BytesIO(self.blend)) as f:
					self.blend = f.read()
			except IOError as e:
				pass
			
		try:
			self._dict = json.loads(str(package.read(self._config), encoding='utf8'))
		except ValueError as e:
			print(self._config)
			raise PackageError("Problem parsing the JSON file: "+str(e))
		
		# This is used for handling temporary image files
		self._image = None
		
		# Store the path for possible later use
		self._path = path
		
		# Store the package
		self._package = package
		
		# Validate the file
		self._validate()
		
	@classmethod
	def create(cls, package_name):
		path = cls._dir + '/' + package_name
		
		try:
			os.mkdir(path)
			
			new_file = cls._schema.split('.')
			new_file[0] += '_new'
			shutil.copyfile('.'.join(new_file), path+'/'+cls._config)
			
			# Create an empty blendfile
			if cls._blend:
				open(path+'/'+cls._blend, "wb").close()
				
			# Create an empty image file
			if cls._img:
				open(path+'/'+cls._img, "wb").close()
			
			return cls(package_name)
		except Exception as e:
			print(e)
			print("Unable to create package in "+path)
		
		return None
		
	@classmethod
	def get_package_list(cls):
		packages = []
		
		for f in os.listdir(cls._dir):
			if f.startswith('.'): continue
		
			if os.path.isdir(os.path.join(cls._dir, f)) or f.endswith(cls._ext):
				try:
					packages.append(cls(f.replace("."+cls._ext, "")))
				except Exception as e:
					print(f, e)
				
		return packages
	
		# return [cls(p) for p in os.listdir(cls._dir) if os.path.isdir(p) and not p.startswith('.')]
		
	def _validate(self):
		if not self._schema:
			# raise PackageWarning
			print("No schema found for {0}, not validating".format(self._path))
			return
		
		schema = {}
		
		# First load the parent_schema if there is one
		if self._parent_schema:
			with open(self._parent_schema) as f:
				schema.update(json.loads(f.read()))
				
		# Then load the schema (this overwrites old keys)
		with open(self._schema) as f:
			schema.update(json.loads(f.read()))
		
		for key, value in schema.items():
			if not self._validate_dict(self._dict, key, value):
				del self._dict[key]
				
	def _validate_dict(self, d, key, value, setting=True):
		if key not in d:
			print("\"{0}\" is missing from {1}".format(key, self._path.replace('/', ':')))
			return False
		elif isinstance(value, dict):
			if not setting:
				# This stucture is too nested, break out
				return False
			else:
				l = []
				for item in d[key]:
					good = True
					for k, v in value.items():
						if not self._validate_dict(item, k, v, setting=False):
							good = False
							break
					if good: l.append(item)
						
				setattr(self, key, l)
				
				# We set here, so return True
				return True
		elif isinstance(eval(value), set):
			items = eval(value)
			
			if d[key] not in items:
				print("Expected item in {0} for {1}, got \"{2}\" instead".format(items, key, d[key]))
				return False
			
			if setting:
				setattr(self, key, self._dict[key])
			
			return True
		elif not isinstance(d[key], eval(value)):
			print("Expected {0} for {1}, got {2} instead".format(value, key, type(self._dict[key])))
			return False
		else:
			# Passed all tests, assign as an attribute
			if setting:
				setattr(self, key, self._dict[key])
			return True
			
	def pack(self, path):
		zip = zipfile.ZipFile(path+'.'+self._ext, "w", zipfile.ZIP_DEFLATED)
		
		# Write config
		zip.write(os.path.join(self._path, self._config), arcname=self._config)
		
		# Write blend
		if self._blend:
			zip.write(os.path.join(self._path, self._blend), arcname=self._blend)
			
		# Write image
		if self._img:
			zip.write(os.path.join(self._path, self._img), arcname=self._img)
			
		zip.close()
		
	def write(self):
		"""Write the archive file back out to disk"""
		
		# Only do the config for now
		
		# First we need the dictionary filled with the newest values
		for key in self._dict:
			self._dict[key] = getattr(self, key)
			
		config = json.dumps(self._dict, sort_keys=True, indent=4)
		
		with open(self._path+'/'+self._config, 'w') as f:
			f.write(config)

	def open_image(self):		
		# If there is an image file, copy it to a temp location
		if self._img:
			# Remove any previously opened images
			if self._image:
				self._image.file.close()
				os.remove(self._image.name)
				
			self._image = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
			self._image.write(self._package.read(self._img))
			
			return self._image.name
		
		# No image, return None
		return None
		
	def close_image(self):
		if self._image:
			self._image.file.close()
			os.remove(self._image.name)
			self._image = None
				
class Map(Package):
	"""Map package"""
	
	_ext = 'map'
	_blend = 'map.blend'
	_config = 'map.json'
	_schema = 'Schemas/mapfile.json'
	_dir = 'Maps'
	
class EncounterDeck(Package):
	"""Encounter deck package"""
	
	def __init__(self, package_name):
		Package.__init__(self, package_name)
		
		# Build a deck
		self.deck = []
		
		for card in self.cards:
			self.deck.extend([(card['monster'], card['role']) for i in range(card['count'])])
	
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
	_dir = 'Powers'
	
	def __init__(self, package_name):
		Package.__init__(self, package_name)
		
		# Write the script to a temp file
		pyfile = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
		pyfile.write(self._package.read("power.py"))
		pyfile.read() # Not sure why this is needed, but the module isn't properly loaded otherwise
		
		# Load the module
		p = imp.load_source("power", pyfile.name)
		
		# We don't need the temp file anymore, so clean up
		pyfile.close()
		os.remove(pyfile.name)
		os.remove(pyfile.name.replace('.py', '.pyc'))

		# Grab the method from the module
		self._use = p.power
		
	def use(self, controller, user):
		self._use(self, controller, user)
		
	def pack(self, path):
		Package.pack(self, path)
		
		zip = zipfile.ZipFile(path+'.'+self._ext, "a", zipfile.ZIP_DEFLATED)
		
		# Copy py file
		zip.write(os.path.join(self._path, 'power.py'), arcname='power.py')
		
		zip.close()
		
class Item(Package):
	"""Item Package"""
	
	_ext = 'item'
	_config = 'item.json'
	_schema = 'Schemas/itemfile.json'
	_new = 'Schemas/itemfile_new.json'
	_dir = 'Items/Others'
	
class Weapon(Item):
	"""Weapon Package"""
	
	_config = 'weapon.json'
	_blend = 'weapon.blend'
	_parent_schema = Item._schema
	_schema = 'Schemas/weaponfile.json'
	_dir = 'Items/Weapons'
	
	def __init__(self, package_name):
		Item.__init__(self, package_name)
		
		# Store the original damage string for possible error printing
		_damage = self.damage
		
		# Split the damage into two parts, separated by a 'd'
		self.damage = [int(i) for i in self.damage.split('d')]
		
		if len(self.damage) != 2:
			raise PackageError("Malformed damage for Weapon. Expected xdy, got {0} instead".format(_damage))
			
	def write(self):
		# Store the original value so we can restore it
		_damage = self.damage
		
		self.damage = 'd'.join([str(self.damage[0]), str(self.damage[1])])
		
		Item.write(self)
		
		self.damage = _damage
	
class Armor(Item):
	"""Armor Package"""
	
	_config = 'armor.json'
	_parent_schema = Item._schema
	_schema = 'Schemas/armorfile.json'
	_dir = 'Items/Armors'
	
class ActionSet(Item):
	"""Action Set Package"""
	
	_ext = 'as'
	_blend = 'actionset.blend'
	_config = 'actionset.json'
	_schema = 'Schemas/actionsetfile.json'
	_new = 'Schemas/actionsetfile_new.json'
	_dir = 'Actions'