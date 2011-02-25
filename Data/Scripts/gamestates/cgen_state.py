# $Id$

from Scripts.packages import *
from Scripts.character_logic import PlayerLogic
from Scripts.power_manager import *
from Scripts.inventory import *
from .base_state import BaseState, BaseController


class CharacterCreationState(BaseState, BaseController):
	"""A state that handles creating a new character"""
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['last_layout'] = ''
		main['next_layout'] = 'cgen_select'
		main['cgen_input'] = {}
		main['creation_done'] = False
		
		# Load the ui
		main['ui_system'].load_layout(main['next_layout'])
		
	def client_run(self, main):
		"""Client-side run method"""
		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
		
		# Check for cgen start
		if main['next_layout'] == 'start' and main['cgen_input']['character'].package_name == "&new":
			main['next_layout'] = 'cgen_name'
		
		# Check for cgen end
		elif main['next_layout'] in ('end_cgen', 'start'):	
			# Add the player empty
			gameobj = main['engine'].add_object("CharacterEmpty")
	
			# Load the target shapes
			main['target_shapes'] = {}
			for child in gameobj.children:
				if child.name == "blast":
					main['target_shapes']['BLAST'] = child
				elif child.name == "burst":
					main['target_shapes']['BURST'] = child
			
			# Setup the player logic
			player = PlayerLogic(gameobj)
			
			race = None
			if main['next_layout'] == 'start':
				player.load(main['cgen_input']['character'])
				race = player.race
			else:
				race = main['cgen_input']['race']
				
			# Now add the mesh and armature based on race data
			main['engine'].load_library(race)
			
			root_ob = main['engine'].add_object(race.root_object)
			root_ob.position = gameobj.position
			root_ob.set_parent(gameobj)
			
			# Setup the armature
			gameobj.armature = root_ob
			
			if main['next_layout'] == 'end_cgen':
				# Set the player's name
				player.name = main['cgen_input']['name']
				
				# Set the player's race
				player.race = main['cgen_input']['race']
				
				# Set the player's class
				player.player_class = main['cgen_input']['class']			
				
				# This levels the player to 1
				player.xp += 0
				
				# Set the player's abilities
				player.str_ab = 10
				player.con_ab = 10
				player.dex_ab = 10
				player.int_ab = 10
				player.wis_ab = 10
				player.cha_ab = 10
				
				player.speed_base = 5
				
				# Now it is time to fill in the rest of the stats
				player.recalc_stats()
				
				# Give the player an attack power
				player.powers.add(Power('Attack'), self)
				
				# Give the player racial traits
				# This needs to be done after giving the player xp to ensure there
				# is already an unspent level for level 1
				traits = player.race.traits
				try:
					player.powers.add(Feat(traits), self)
				except PackageError:
					print("Unable to open up the file %s for %s's racial traits" % (traits, player.race.name))
				
				# Setup player inventory
				player.inventory = Inventory()
				
				w = Weapon('Longsword')
				player.inventory.add(w)
				player.inventory.weapon = w
				
				
				a = Armor('Mighty Robes')
				player.inventory.add(a)
				player.inventory.armor = a
					
				player.inventory.add(Item('Bonsai'))
				
				# Give the player some starting credits
				player.inventory.credits = 100
				
				# Save the new player
				player.save()
			
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
		
		# Check for game start
		elif False and main['next_layout'] == 'start':
			
			# Add the player empty
			gameobj = main['engine'].add_object("CharacterEmpty")
			
			# Setup the player logic
			player = PlayerLogic(gameobj)
			player.load(main['cgen_input']['character'])
			
			# Now add the mesh and armature based on race data
			race = player.race
			main['engine'].load_library(race)
			
			root_ob = main['engine'].add_object(race.root_object)
			root_ob.position = gameobj.position
			root_ob.set_parent(gameobj)
			
			# Setup the armature
			gameobj.armature = root_ob
			
			main['net_players'][main['client'].id] = player
			main['player'] = player
			
			# Fill the player's hit points
			player.hp = player.max_hp
			
			# Set up the camera
			from Scripts.blender_wrapper import Camera
			camera_pivot = main['engine'].add_object("pivot")
			main['camera'] = Camera(camera_pivot, main['player'].object)
			
			return ("DungeonGeneration", "SWITCH")
		
		# If the set layout differs from the previous layout, switch to the new layout.
		# The new current layout is saved in last layout to continue checking.
		if main['next_layout'] != main['last_layout']:
			main['last_layout'] = main['next_layout']
			main['ui_system'].load_layout(main['next_layout'])
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		# We added these so we need to get rid of them too
		
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