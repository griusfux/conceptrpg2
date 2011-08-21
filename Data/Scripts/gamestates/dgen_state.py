# $Id$

from Scripts.packages import Map, Shop
from .base_state import *

import time

class DungeonGenerationState(BaseState):
	"""A state used to build dungeons"""
	
	client_functions = BaseState.client_functions.copy()
	server_functions = BaseState.server_functions.copy()
			
	##########
	# Client
	##########
	
	# Client RPC functions
	@rpc(client_functions, "load_dungeon", int, int, "pickle")
	def load_dungeon(self, main, idx, max, dungeon_tile):
		self.dungeon_list.append(dungeon_tile)
		self.tiles_recv.add(idx)
		if max > self.max_tiles:
			self.max_tiles = max
		
	@rpc(client_functions, "finish_dungeon")
	def finish_dungeon(self, main):
		if len(self.tiles_recv) < self.max_tiles:
			# We missed some, try to grab them
			missing = set([i for i in range(self.max_tiles)]) - self.tiles_recv
			self.server.invoke('request_dungeon_pieces', missing)
		else:
			main['dgen'].generate_from_list(main, self.dungeon_list)
			print("Dungoen downloaded from the server")
			self.building = False
		
	@rpc(client_functions, "build_dungeon")
	def build_dungeon(self, main):
		self.send_dungeon = True
	
	def client_init(self, main):
		"""Intialize the client state"""
		# Import the generator here so the server won't complain
		from Scripts.dungeon_generator import DungeonGenerator
		
		# Show the loading screen
		main['ui_system'].load_layout('dun_gen')
		
		# Load up the map file and load the scene
		self.map = Map('Mines')
		main['engine'].load_library(self.map)
		
		# We want to time the generator
		self.start_time = time.time()
		
		# Now startup the generator
		if 'dgen' not in main:
			main['dgen'] = DungeonGenerator(self.map)
		else:
			main['dgen'].clear()
		
		# Save an encounter deck
		main['encounter_deck'] = self.map.encounter_deck
		
		# A list of tiles to generate a dungeon from if we recieve one from the server
		self.dungeon_list = []
		self.max_tiles = -1
		self.tiles_recv = set()
		
		# A flag to know if we are still building the dungeon
		self.building = True
		
		# A flag to know if we should send the dungeon to the server
		self.send_dungeon = False
		
		# Now request a dungeon from the server
		self.server.invoke('request_dungeon')
		
	def client_run(self, main):
		"""Client-side run method"""
		
		if self.building:
			# If we have tiles in the dungeon list, then don't build
			if self.dungeon_list:
				return
		
			# Assume we're building a dungeon unless we are told otherwise
			if not main['dgen'].result:
				main['dgen'].generate_first(main)
			elif main['dgen'].has_next():
				main['dgen'].generate_next()
				return
			elif not main['dgen'].check_dungeon():
				# Clear the tiles and restart the generator
				main['dgen'].clear()
				return
			elif self.send_dungeon:
				# We finished, send the map to the server and continue
				self.server.invoke('save_dungeon')
				for i in main['dgen'].result:
					self.server.invoke('update_dungeon', i)
				self.server.invoke('finish_dungeon')
				self.building = False
			# else:
				# raise SystemError("Built a dungeon, but the server didn't request one nor was a dungeon received from the server.")
		else:
			# Dungeon is done
			print("\nDungeon generation complete with %d rooms\n in %.4f seconds" % (main['dgen'].room_count, time.time() - self.start_time))
			
			# Move the player to the start tile
			pos = main['dgen']._tiles[0].position
			pos[2] += 1
			main['player'].object.position = pos
			
			# Add the shop keeper
			if (main['dgen'].shop_node):
				shop_node = main['dgen'].shop_node
				shop = Shop(self.map.shop)
				main['engine'].load_library(shop)
				shop_obj = main['engine'].add_object(shop.root_object, shop_node.position)
				shop_obj.set_orientation(shop_node.orientation)
				main['shop_keepers'] = {shop: shop_obj}
			else:
				main['shop_keepers'] = {}
				print("Could not find a shop empty!")
			
			# Add the player to the server state
			pobj = main['player'].object
			pos = pobj.position[:]
			ori = [[a, b, c] for a, b, c in pobj.get_orientation()]
			self.server.invoke('add_player', main['player'].get_info(), pos, ori)
			
			
			main['engine'].stop_bgm()
			
			# Switch to the default state now
			self.server.invoke('switch_state', "Default")
			return ("Default", "SWITCH")
			
	##########
	# Server
	##########
			
	# Server RPC functions
	@rpc(server_functions, "request_dungeon")
	def request_dungeon(self, main, client):
		if main['dungeon']:
			self.send_dungeon(main, client)
		else:
			self.client.invoke('build_dungeon')
			
	@rpc(server_functions, "request_dungeon_pieces", "pickle")
	def request_dungeon_pieces(self, main, client, missing):
		if main['dungeon']:
			self.send_dungeon(main, client, missing)
		
	@rpc(server_functions, "save_dungeon")	
	def save_dungeon(self, main, client):
		# This creates a "lock" on editing the dungeon
		if not main['dungeon']:
			main['dungeon_lock'] = client.id
		else:
			print("Recieved a save dungeon request from %s, but a dungeon was already built" % client.id)
			self.send_dungeon(main, client)
		
	@rpc(server_functions, "update_dungeon", "pickle")
	def update_dungeon(self, main, client, tile):
		if client.id != main.get("dungeon_lock"):
			print("Recieved an update dungeon request from %s, but the client didn't lock the dungeon" % client.id)
			self.send_dungeon(main, client)
		else:
			main['dungeon'].append(tile)
			
			# Add an encounter if we have a room
			if tile[0] == "Rooms":
				main['encounters'][str(tile[2])] = True
	
	@rpc(server_functions, "finish_dungeon")		
	def finish_dungeon(self, main, client):
		# This releases the lock on the dungeon
		if client.id == main.get("dungeon_lock"):
			del main['dungeon_lock']
			print("Dungeon uploaded by", client.id)
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""
		pass
	
	def send_dungeon(self, main, client, missing=None):
		print("Dungeon download begun for", client.id)
		
		tiles_sent = 0
		
		if not missing:
			missing = set([i for i in range(len(main['dungeon']))])
		
		for i, v in enumerate(main['dungeon']):
			if i in missing:
				self.client.invoke('load_dungeon', i, len(main['dungeon']), v)
				# We wait a little bit so the BGE can keep up
				time.sleep(0.01)
				tiles_sent += 1
				
		print("Finished sending %d tiles to %s" % (tiles_sent, client.id))
		
		self.client.invoke('finish_dungeon')

	##########
	# Other
	##########