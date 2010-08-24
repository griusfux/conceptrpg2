# try:
	# import lxml.etree as etree
	# print('Lxml detected, xml validation enabled')
	# XMLSyntaxError = etree.XMLSyntaxError
	# VALIDATING = True
# except ImportError:
import xml.etree.ElementTree as etree
XMLSyntaxError = SyntaxError
VALIDATING = False

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
	_dir = ''
	
	root = None
	init = False
	
	def __init__(self, _filename):
		parser = etree.XMLParser()
		self.root = None

		filename = self._dir+'/'+_filename
		self.origin = filename
		self.is_zip = False
		
		# If the file is packed, extract the files to a tmp location
		if not os.path.exists(filename) and os.path.exists(filename+"."+self._ext):
			zfile = ZipFile(filename+"."+self._ext, 'r')	
			filename = 'tmp/'+filename
			self.is_zip = True
			
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
			if VALIDATING:
				dtd = etree.DTD(file=self._dtd)
				if not dtd.validate(tree.getroot()):
					print("\nValidation Error:")
					print(dtd.error_log)
				else:
					self.root = tree.getroot()
					self.init = True
			else:
				self.root = tree.getroot()
				self.init = True
		except XMLSyntaxError as e:
			if VALIDATING:
				print("Syntax Error:")
				print(parser.error_log)
			else:
				print(e)
			print("\nError with config file from "+_filename+"!")
		except IOError:
			print("Error in opening the config file: "+self.config)
			
	def __del__(self):
		# Try to cleanup
		self.close()

	def close(self):
		"""Clean up"""
		if self.file_name.startswith('tmp/'):
			shutil.rmtree(self.file_name, ignore_errors=True)
			
			# Try to remove the _dir directory
			try:
				os.rmdir('tmp/'+self._dir)
			except OSError:
				pass
			
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
	_dir = 'Maps'
	
	
class ClassFile(ArchiveFile):
	"""Class for handling the player class files"""
	# Options for the archive file
	_ext = 'class'
	_blend = ""
	_textures = ""
	_config = 'class.xml'
	_dtd = 'Schemas/classfile.xml'
	_dir = 'Classes'
	
class RaceFile(ArchiveFile):
	"""Class for handling the race files"""
	# Options for the archive file
	_ext = 'race'
	_blend = "race.blend"
	_textures = ""
	_config = 'race.xml'
	_dtd = 'Schemas/racefile.xml'
	_dir = 'Races'
	
class MonsterFile(ArchiveFile):
	"""Class for handling monster files"""
	#Options for the archive file
	_ext = 'monster'
	_blend = 'monster.blend'
	_textures = ""
	_config = 'monster.xml'
	_dtd = 'Schemas/monsterfile.xml'
	_dir = 'Monsters'
		
class DeckFile(ArchiveFile):
	"""Class for handling Encounter Deck files"""
	#Options for the archive file
	_ext = 'deck'
	_blend = ""
	_textures = ""
	_config = 'deck.xml'
	_dtd = 'Schemas/deckfile.xml'
	_dir = 'EncounterDecks'
	
class ArmorFile(ArchiveFile):
	"""Class for handling the armor files"""
	# Options for the archive file
	_ext = 'armor'
	_blend = ""
	_textures = ""
	_config = 'armor.xml'
	_dtd = 'Schemas/armorfile.xml'
	_dir = 'Items/Armors'

class ShieldFile(ArchiveFile):
	"""Class for handling the shield files"""
	# Options for the archive file
	_ext = 'shield'
	_blend = ""
	_textures = ""
	_config = 'shield.xml'
	_dtd = 'Schemas/shieldfile.xml'
	_dir = 'Items/Shields'
	
class WeaponFile(ArchiveFile):
	"""Class for handling the weapon files"""
	# Options for the archive file
	_ext = 'weapon'
	_blend = ""
	_textures = ""
	_config = 'weapon.xml'
	_dtd = 'Schemas/weaponfile.xml'
	_dir = 'Items/Weapons'
	
class PowerFile(ArchiveFile):
	"""Class for handling power files"""
	#Options for the archive file
	_ext = 'power'
	_blender = ''
	_textures = ''
	_config = 'power.xml'
	_dtd = 'Schemas/powerfile.xml'
	_dir = 'Powers'