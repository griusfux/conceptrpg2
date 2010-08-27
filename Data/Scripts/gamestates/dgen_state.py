# $Id$

from Scripts.packages import Map
from .base_state import BaseState

import time

class DungeonGenerationState(BaseState):
	"""A state used to build dungeons"""
	
	def __init__(self, main, is_server=False):
		"""DungeonBuildingState constructor"""
		
		BaseState.__init__(self, main, is_server)
			
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		# Import the generator here so the server won't complain
		from Scripts.dungeon_generator import DungeonGenerator
		
		# Show the loading screen
		main['ui_system'].load_layout('dun_gen')
		
		# Load up the map file and load the scene
		map = Map('ShipRuins')
		main['engine'].load_library(map)
		
		# We want to time the generator
		self.start_time = time.time()
		
		# Now startup the generator
		if 'dgen' not in main:
			main['dgen'] = DungeonGenerator(map)
		else:
			main['dgen'].clear()
		
		# Save an encounter deck
		main['encounter_deck'] = map.encounter_deck
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# Keep our connection to the server up
		main['client'].send('')
		
		if not main['dgen'].rooms:
			main['dgen'].generate_first(main)
		elif main['dgen'].has_next():
			main['dgen'].generate_next()
			return
		elif not main['dgen'].check_dungeon():
			# Clear the tiles and restart the generator
			main['dgen'].clear()
			return
		else:
			# Dungeon is done
			print("\nDungeon generation complete with %d rooms\n in %.4f seconds" % (main['dgen'].room_count, time.time() - self.start_time))
			
			# Move the player to the start tile
			pos = main['dgen']._tiles[0].get_position()
			pos[2] += 0.5
			main['player'].obj.set_position(pos)
			
			# Switch to the default state now
			return ("Default", "SWITCH")
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main):
		"""Server-side run method"""
		pass

	##########
	# Other
	##########
	
	# Empty ---
	