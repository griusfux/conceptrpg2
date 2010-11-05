# $Id$

from Scripts.packages import *
from Scripts.character_logic import PlayerLogic
from Scripts.power_manager import *
from Scripts.inventory import *
from .base_state import BaseState


class CharacterCreationState(BaseState):
	"""A state that handles creating a new character"""
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		# Load some packages for the ui to make use of
		main['races'] = Race.get_package_list()
		main['classes'] = Class.get_package_list()
		
		main['last_layout'] = 'char_creation'
		main['next_layout'] = 'cgen_name'
		main['cgen_input'] = {}
		main['creation_done'] = False
		
		# Load the ui
		main['ui_system'].load_layout(main['next_layout'])
		
	def client_run(self, main):
		"""Client-side run method"""
		
		inputs = main['input_system'].run()
		
		if main['next_layout'] == 'start' or ("Jump", "INPUT_CLICK") in inputs:
			
			# Add the player empty
			gameobj = main['engine'].add_object("CharacterEmpty")
			
			# Now add the mesh and armature based on race data
			race = Race("DarkKnight")
			main['engine'].load_library(race)
			
			root_ob = main['engine'].add_object(race.root_object)
			root_ob.position = gameobj.position
			root_ob.set_parent(gameobj)
			
			# Setup the armature
			gameobj.armature = root_ob
			
			# Setup the player logic
			player = PlayerLogic(gameobj)
			
			# Load stats for the player
			player.load_stats(open('Kupoman.save', 'rb'))
			
			# Fill the player's hit points
			player.hp = player.max_hp
			
			# Give the player an attack power
			player.powers = PowerManager([Power('Attack'), Power('Burst')])
			
			# Setup player inventory
			player.inventory = Inventory()
			
			w = Weapon('Holy Hand Grenade')
			player.inventory.add(w)
			player.inventory.weapon = w
			
			a = Armor('Mighty Robes')
			player.inventory.add(a)
			player.inventory.armor = a
				
			player.inventory.add(Item('Bonsai'))
			
			main['net_players'] = {main['client'].id: player}
			main['player'] = player
			
			# XXX The following section needs work to remove BGE-specific code
			import bge
			import Scripts.blender_wrapper as BlenderWrapper
			scene = bge.logic.getCurrentScene()
			
			# Parent the camera to the player
			cam = scene.active_camera
			cam.setParent(scene.objects["TopDownEmpty"])
			cam_empty = scene.objects['CamEmpty']
			
			# Switch to the 3rd person camera
			cam3p = None
			for child in gameobj.gameobj.childrenRecursive:
				if child.name == '3PCam':
					cam3p = child
					break
					
			if cam3p:
				main['3p_cam'] = BlenderWrapper.Camera(cam3p, cam_empty)
				main['top_down_camera'] = BlenderWrapper.Camera(scene.active_camera)
				scene.active_camera = main['3p_cam'].camera
				
			# Switch to the dungeon generation state
			return ("DungeonGeneration", "SWITCH")
		
		# If the set layout differs from the previous layout, switch to the new layout.
		# The new current layout is saved in last layout to continue checking.
		if main['next_layout'] != main['last_layout']:
			main['last_layout'] = main['next_layout']
			main['ui_system'].load_layout(main['next_layout'])
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		# We added these so we need to get rid of them too
		del main['races']
		del main['classes']
		
		del main['last_layout']
		del main['next_layout']
		del main['cgen_input']
		del main['creation_done']
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main):
		"""Server-side run method"""
		pass
			
	def server_cleanup(self, main):
		"""Cleanup the server state"""
		pass

	##########
	# Other
	##########
	
	# Empty ---