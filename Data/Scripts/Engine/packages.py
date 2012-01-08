import json
import pickle
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
	
	def __init__(self, package_name, new_package=False):
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
				raise PackageError("Could not find package: "+package_name+"(%s)"%path)
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
		
		# Store the real name of the package
		self.package_name = package_name
		
		# Store the package
		self._package = package
		
		# Default values for the package (updated in _validate())
		self._defaults = {}
		
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
				shutil.copyfile('Schemas/dummy.png', path+'/'+cls._img)
				# open(path+'/'+cls._img, "wb").close()
			
			return cls(package_name, new_package=True)
		except Exception as e:
			traceback.print_exc()
			print("Unable to create package in "+path)
		
		return None
		
	@classmethod
	def get_package_list(cls, show_traceback=False, sort_date=False):
		packages = []
		
		files = os.listdir(cls._dir)
		
		for file in files:
			if file.startswith('.'):
				files.remove(file)
		
		if sort_date:
			files.sort(key=lambda x: os.stat(cls._dir+'/'+x+'/'+cls._config).st_mtime)
		
		for f in files:
			if f.startswith('.'): continue
		
			if os.path.isdir(os.path.join(cls._dir, f)) or f.endswith(cls._ext):
				try:
					packages.append(cls(f.replace("."+cls._ext, "")))
				except Exception as e:
					if show_traceback:
						traceback.print_exc()
					else:
						print(f, e)
				
		return packages
	
	@classmethod
	def exists(cls, package):
		return os.path.exists(os.path.join(cls._dir, package)) or \
				os.path.exists(os.path.join(cls._dir, package)+"."+cls._ext)
		
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
			
		new_file = self._schema.split('.')
		new_file[0] += '_new'
		with open('.'.join(new_file)) as f:
			self._defaults.update(json.loads(f.read()))
		
#		for key, value in schema.items():
#			if not self._validate_dict(self._dict, key, value):
#				del self._dict[key]
#		print(schema)
		self._validate_dict(self._dict, schema, self._defaults)
		
		for k, v in self._dict.items():
			setattr(self, k, v)
	
	def _validate_dict(self, d, schema, defaults):
		def print_warning(msg):
			name = self._path.replace('/', ':')
			print('WARNING {0}: {1}'.format(name, msg))
		
		# First get rid of any extra items
		invalid = []
		for k, v in d.items():
			if k not in schema:
				print_warning('"{0}" is not a valid key, ignoring'.format(k))
				invalid.append(k)
				
		for k in invalid:
			del d[k]
		
		# Now make sure everything in the schema is accounted for
		for sk, sv in schema.items():
			
			# Check if the key exists
			if sk not in d:
				print_warning('"{0}" not found, setting to default'.format(sk))
				d[sk] =  defaults[sk]
					
			# Handle sub dictionaries
			elif isinstance(sv, dict):
				if not isinstance(d[sk], dict):
					print_warning('Expected a sub dictionary for {0}, got a {1} instead'.format(sk, type(d[sk])))
					d[sk] = defaults[sk]
				else:
					self._validate_dict(d[sk], sv, defaults[sk])
					
			# Handle lists
			elif isinstance(sv, list):
				if not isinstance(d[sk], list):
					print_warning('Expected a list for {0}, got a {1} instead'.format(sk, type(d[sk])))
					d[sk] = defaults[sk]
				else:
					for i in d[sk]:
						self._validate_dict(i, sv[0], defaults[sk][0])
				
			# Handle sets
			elif isinstance(eval(sv), set):
				items = eval(sv)
				if d[sk] not in items:
					print_warning('Expected item in {0} for {1}, got "{2}" instead'.format(items, sk, d[sk]))
					d[sk] = defaults[sk]
			
			# Handle everything else
			elif not isinstance(d[sk], eval(sv)):
				print_warning('Expected a {0} for {1}, got {2} instead'.format(type(eval(sv)), sk, type(d[sk])))
				d[sk] = defaults[sk]
				
	def __validate_dict(self, d, key, value, setting=True):
		if key not in d:
			print("\"{0}\" is missing from {1}".format(key, self._path.replace('/', ':')))
			if key in self._defaults:
				# Add the key to the dict
				self._dict[key] = self._defaults[key]
				if setting:
					setattr(self, key, self._dict[key])
				return True
			else:
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
			
			# I'm not sure why, but reading the file helps prevent lock ups with the OS
			self._image.read()
			
			return self._image.name
		
		# No image, return None
		return None
		
	def close_image(self):
		if self._image:
			self._image.file.close()
			os.remove(self._image.name)
			self._image = None
				
