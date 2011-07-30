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
		self.saves = Package.Save.get_package_list(sort_date=True)[::-1]
			
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

		main['player'] = None

		main['csl_continue'] = False
		main['csl_new'] = False
		main['csl_char'] = None
													
			
	def client_run(self, main):
		"""Client-side run method"""		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenue", "PUSH")		
		
		# Lets add a little bit of movement
		idle = main['default_actions']['default_idle']
		for i in range(min(len(self.characters), 4)):
			self.characters[i].object.play_animation(idle['name'], idle['start'],
													idle['end'], mode=1)
		
		if main['csl_new']:
			return("CharacterCreation", "SWITCH")
		
		if main['csl_continue']:	
			# Add the player empty
			gameobj = main['engine'].add_object("CharacterEmpty")
	
			# Load the target shapes
			main['target_shapes'] = {}
			for child in gameobj.children:
				if child.name == "blast":
					main['target_shapes']['BLAST'] = child
				elif child.name == "burst":
					main['target_shapes']['BURST'] = child
					
			player = self.characters[0]
			main['net_players'] = {main['client'].id: player}
			main['player'] = player
			player.id = main['client'].id
			
			# Fill the player's hit points
			player.hp = player.max_hp
			
			# Set up the camera
			from Scripts.blender_wrapper import Camera
			camera_pivot = main['engine'].add_object("pivot")
			main['camera'] = Camera(camera_pivot, main['player'].object)
			
			return ("DungeonGeneration", "SWITCH")
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['engine'].remove_object(self.scene)
		for character in self.characters:
			if character == main['player']:
				continue
			main['engine'].remove_object(character.object)

		del main['csl_continue']
		del main['csl_new']
		del main['csl_char']