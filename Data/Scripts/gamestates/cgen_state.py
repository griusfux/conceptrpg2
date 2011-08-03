# $Id$

from Scripts.packages import *
from Scripts.character_logic import PlayerLogic
from Scripts.power_manager import *
from Scripts.inventory import *
from .base_state import BaseState, BaseController
import Scripts.items as Items


class CharacterCreationState(BaseState, BaseController):
	"""A state that handles creating a new character"""
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['cgen_data'] = None
		main['cgen_exit'] = False
		
		# Load the ui
		main['ui_system'].load_layout("CharGenLayout")
		
		# Setup the camera
		self.scene = main['engine'].add_object("char_gen", (0,0,0), (0,0,0))
		main['engine'].set_active_camera("char_gen_camera")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
		
		# Check for cgen end
		if main['cgen_exit']:
			
			if main['cgen_data']:
				player = PlayerLogic(None)
				
				# Set the player's name
				player.name = main['cgen_data']['name']
						
				# Set the player's race
				player.race = main['cgen_data']['race']
				
				# Set the player's class
				player.player_class = main['cgen_data']['class']
				
				# Set the player's element
				player.element = main['cgen_data']['element']	
				
				# This levels the player to 1
				player.xp += 0
				
				
				player.max_hp = 16
				player.speed = 5
				
				# Now it is time to fill in the rest of the stats
				player.recalc_stats()
				
				# Give the player an attack power
				player.powers.add(Power('Attack'), self)
				
				# Give the player racial traits
				# This needs to be done after giving the player xp to ensure there
				# is already an unspent level for level 1
				if player.race.traits:
					traits = player.race.traits
					try:
						player.powers.add(Feat(traits), self)
					except PackageError:
						print("Unable to open up the file %s for %s's racial traits" % (traits, player.race.name))
				
				# Setup player inventory
				
				w = Items.Weapon('Longsword', 5)
				player.inventory.append(w)
				player.weapon = w
				
				
				a = Items.Armor('Robes', 5)
				player.inventory.append(a)
				player.armor = a
				
				player.save()

			return("CharacterSelect", "SWITCH")
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		self.scene.end()
		
		# We added these so we need to get rid of them too
		del main['cgen_data']
		del main['cgen_exit']
			
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