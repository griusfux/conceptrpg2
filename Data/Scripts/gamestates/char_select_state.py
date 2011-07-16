import math

from .base_state import BaseState, BaseController
import Scripts.packages as Package
import Scripts.character_logic as Character
_POSITIONS = 	[
					(0, 0, 0.2),
					(1.170, 3.214, 0.2),
					(4.132, 4.924, 0.2),
					(7.500, 4.330, 0.2),
				]

class CharacterSelectState(BaseState, BaseController):
	"""A state for the title screen"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		# Load the ui
		main['ui_system'].load_layout("CharSelectLayout")
		
		# Setup the camera
		self.scene = main['engine'].add_object("char_select", (0,0,0), (0,0,0))
		main['engine'].set_active_camera("char_select_camera")
		
		# Get the saves
		self.saves = Package.Save.get_package_list()
			
		self.characters = []
		for save in self.saves:
			if save.name == "New Character":
				continue
			character = Character.PlayerLogic(None)
			character.load(save)
			
			main['engine'].load_library(character.race)
			obj = main['engine'].add_object(character.race.root_object,
											(42,0,0), (0,0,math.radians(180)))
			obj.armature = obj
			character.object = obj
			
			self.characters.append(character)

		for i in range(min(len(self.characters), 4)):
			self.characters[i].object.position = _POSITIONS[i]
													
			
	def client_run(self, main):
		"""Client-side run method"""		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("CharacterCreation", "SWITCH")
		
		
		# Lets add a little bit of movement
		idle = main['default_actions']['default_idle']
		for i in range(min(len(self.characters), 4)):
			self.characters[i].object.play_animation(idle['name'], idle['start'],
													idle['end'], mode=1)
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['engine'].remove_object(self.scene)
		for character in self.characters:
			main['engine'].remove_object(character.object)
