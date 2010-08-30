# $Id$

import json
import os
import zipfile
import gzip
import io

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
	_dir = ''
	
	def __init__(self, package_name):
		# Combine the package name and the directory to get the filepath
		path = self._dir + '/' + package_name
		
		# Check to see if the file is packed (unpacked takes precedence)
		if not os.path.exists(path):
			if os.path.exists(path+'.'+self._ext):
				path += '.'+self._ext
				package = zipfile.ZipFile(path)
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
		
		# Store the path for possible later use
		self._path = path
		
		# Validate the file
		self._validate()
		
	def _validate(self):
		if not self._schema:
			# raise PackageWarning
			print("No schema found for {0}, not validating".format(self._path))
			return
			
		with open(self._schema) as f:
			schema = json.loads(f.read())
		
		for key, value in schema.items():
			self._validate_dict(self._dict, key, value)
				
	def _validate_dict(self, d, key, value, setting=True):
		if key not in d:
			print("\"{0}\" is missing from {1}".format(key, self._path.replace('/', ':')))
			return False
		elif isinstance(value, dict):
			if not setting:
				# This stucture is too nest, break out
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
				
				# We set here, so return False
				return False
		elif not isinstance(d[key], eval(value)):
			print("Expected {0} for {1}, got {2} instead".format(value, key, type(self._dict[key])))
			return False
		else:
			# Passed all tests, assign as an attribute
			if setting:
				setattr(self, key, self._dict[key])
			return True

			
				
class Map(Package):
	"""Map package"""
	
	_ext = 'map'
	_blend = 'map.blend'
	_config = 'map.json'
	_schema = 'Schemas/mapfile.json'
	_dir = 'Maps'
	
class Race(Package):
	"""Race package"""
	
	_ext = 'race'
	_blend = 'race.blend'
	_config = 'race.json'
	_schema = 'Schemas/racefile.json'
	_dir = 'Races'

class Power(Package):
	"""Power package"""
	
	_ext = 'power'
	_blend = ''
	_config = 'power.json'
	_schema = 'Schemas/powerfile.json'
	_dir = 'Powers'
	
	def __init__(self, package_name):
		Package.__init__(self, package_name)
		
		import sys
		sys.path.append(self._path)
		import power
		self._use = power.power
		
		sys.path.remove(self._path)
		
	def use(self, state, user, target):
		self._use(self, state, user, target)