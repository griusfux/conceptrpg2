import xml.etree.cElementTree as etree
from zipfile import *
import os
import shutil

class ArchiveFile:
	"""Base archive class"""
	# Options for the archive file
	_ext = 'zip'
	_blend = ''
	_textures = 'textures/'
	_config = ''
	_dtd = ''
	
	Root = None
	Init = False
	
	def __init__(self, filename):
		parser = etree.XMLParser()
		self.Root = None

		# If the file is packed, extract the files to a tmp location
		if os.path.exists(filename+"."+self._ext):
			zfile = ZipFile(filename+"."+self._ext, 'r')	
			filename = 'tmp/'+filename
			
			zfile.extract(self._config,  filename)
			if self._blend:
				zfile.extract(self._blend,  filename)
			
			# Unpack the texture folder
			for texture in [f  for f in zfile.namelist() if f.startswith(self._textures)]:
				zfile.extract(texture, filename)


		# Store the locations for later use
		self.file_name = filename
		self.blend = filename+'/'+self._blend
		self.config = filename+'/'+self._config

		# Try and load the xml file and validate it		
		try:
			tree = etree.parse(self.config, parser)
			# dtd = etree.DTD(file=self._dtd)
			# if not dtd.validate(tree.getroot()):
				# print("Validation Error:")
				# print(dtd.error_log)
				# raise etree.DTDValidateError("")
			# dtd.validate(tree.getroot())
			self.root = tree.getroot()
			self.init = True
		# except(etree.XMLSyntaxError):
			# print("Syntax Error:")
			# print(parser.error_log)
			# print("\nError with config file from "+filename+"!")
		# except(etree.DTDValidateError):
			# print("\nError with config file from "+filename+"!")
		except(IOError):
			print("Error in opening the config file")

	def Close(self):
		"""Clean up"""
		if self.file_name.startswith('tmp/'):
			shutil.rmtree(self.file_name, ignore_errors=True)
			
			# Try and remove the tmp dir. If this fails, other files are still in it
			try:
				os.rmdir('tmp')
			except OSError:
				pass # Just leave it alone
				

class MapFile(ArchiveFile):
	"""Class for reading map files"""
	# Options for the archive file
	_ext = 'map'
	_blend = 'map.blend'
	_textures = 'textures/'
	_config = 'map.xml'
	_dtd = 'Schemas/mapfile.xml'
	
class ClassFile(ArchiveFile):
	"""Class for handling the player class files"""
	# Options for the archive file
	_ext = 'class'
	_blend = ""
	_textures = ""
	_config = 'class.xml'
	_dtd = 'Schemas/classfile.xml'
	
class RaceFile(ArchiveFile):
	"""Class for handling the race files"""
	# Options for the archive file
	_ext = 'race'
	_blend = ""
	_textures = ""
	_config = 'race.xml'
	_dtd = 'Schemas/racefile.xml'
		
class ArmorFile(ArchiveFile):
	"""Class for handling the armor files"""
	# Options for the archive file
	_ext = 'armor'
	_blend = ""
	_textures = ""
	_config = 'armor.xml'
	_dtd = 'Schemas/armorfile.xml'

class ShieldFile(ArchiveFile):
	"""Class for handling the shield files"""
	# Options for the archive file
	_ext = 'shield'
	_blend = ""
	_textures = ""
	_config = 'shield.xml'
	_dtd = 'Schemas/shieldfile.xml'