# $Id$

import random
import GameLogic
import Scripts.blender_wrapper as BlenderWrapper
from mathutils import Vector, Matrix
from Scripts.packages import EncounterDeck

GEN_LINEAR = 0
GEN_RANDOM = 1

# ExitNode types
EN_ROOM = 0
EN_CORR = 1
EN_DOOR = 2

class ExitNode:
	"""A class to store exit node information"""
	
	def __init__(self, obj, type):
		self.object = obj
		self.type = type

class DungeonGenerator:
	"""A class for generating dungeons"""
	
	# Some settings
	max_rooms = 10
	min_rooms = 8
	max_tries = 5
	ray_length = 5
	generation = GEN_RANDOM
	
	def __init__(self, map):	
		# self.tiles is a dictionary of lists
		# The lists are a list of tuples [(obj, scene)]
		self.tiles = {
				'Starts': [i['obj'] for i in map.start_tiles],
				'Rooms': [i['obj'] for i in map.room_tiles],
				'Corridors': [i['obj'] for i in map.corridor_tiles],
				'Ends': [i['obj'] for i in map.end_tiles],
				'Stairs': [i['obj'] for i in map.stair_tiles],
				'Traps': [i['obj'] for i in map.trap_tiles],
				}
				
		self.deck = EncounterDeck(map.encounter_deck)
	
		self._init_values()
		
	def _init_values(self):
		"""Reset the generator to it's original state"""
		# The list of exit nodes
		self.exit_nodes = []
		
		# The list of encounter nodes
		self.encounter_nodes = []
		
		# The current room count
		self.room_count = 0
		
		# The current number of tries to place a tile
		self.tries = 0
		
		# Some flags for the currently placed tiles
		self.has_start = False
		self.has_stairs = False
		
		# Store the KX_Scene object
		self.scene = GameLogic.getCurrentScene()
		
		# This is so we can handle collisions on multiple frames to allow for cleanup
		self.use_as_next_node = None
		
		# This list is the end result of the generator (type, index, position, orientation)
		self.result = []
		
		# This dictionary is used to keep track of what rooms still have encounters in them
		self.rooms = {}
		
		# This is used so we can clear the dungeon if we need to
		self._tiles = []

	def generate_from_list(self, obj, result):
		"""Use a result list to generate the dungeon"""		
		for type, index, position, ori in result:		
			tile = self.tiles[type][index]
			
			# First try to add the object; if it doesn't exist, merge the scene and try again
			# try:
				# tile_node = self.scene.addObject(tile[0], obj)
			# except ValueError:
				# GameLogic.LibLoad(self.blend, 'Scene', tile[1])
				# tile_node = self.scene.addObject(tile[0], obj)
				
			tile_node.worldPosition = position
			tile_node.worldOrientation = ori
			
			if type == "Rooms":
				self.room_count += 1
			elif type == "Stairs":
				self.has_stairs = True
				
		self.result = result
			
	def clear(self):
		"""Get rid of the dungeon created by the generator"""
		for tile in self._tiles:
			tile.end()
			
		self._init_values()
			
	def has_next(self):
		"""Check to see if there are still more exit nodes to fill"""
		return True if self.exit_nodes else False
		
	def generate_first(self, node):
		"""Generate the first tile"""
		
		# Place the start tile
		n = ExitNode(node, EN_ROOM)
		self.exit_nodes.append(n)
		self.place_tile(n, 'Starts')
		
	def generate_next(self):
		"""Generate the next tile"""
		
		random.seed()
	
		# First grab any pending node
		node = self.use_as_next_node
		self.use_as_next_node = None
		
		# Check to see if we should keep expanding the dungeon
		if self.room_count < self.max_rooms:
			if not node:
				# Pick the next node based on options
				if self.generation == GEN_LINEAR:
					index = -1
				else: #GEN_RANDOM
					index = random.randint(0, len(self.exit_nodes) - 1)
					
				node = self.exit_nodes[index]
			
			# Choose a tile to lay down
			roll = random.randint(1, 20)
			tile = None
			
			if node.type == EN_DOOR:
				if roll == 20:
					tile = 'Traps'
				elif roll == 19:
					if not self.has_stairs: tile = 'Stairs'
					else: tile = 'Corridors'
				elif roll < 19 and roll >= 9:
					tile = 'Rooms'
				else:
					tile = 'Corridors'	
			else:
				if roll == 20:
					tile = 'Traps'
				elif roll == 19:
					tile = 'Ends'
				elif roll == 18:
					if not self.has_stairs: tile = 'Stairs'
					else: tile = 'Corridors'
				elif roll < 18 and roll >= 13:
					tile = 'Rooms'
				elif roll <13 and roll >= 10:
					tile = 'Rooms'
				else:
					tile = 'Corridors'
			
			self.place_tile(node, tile)
		else:
			# We are done placing tiles
			
			# Check if we have some stairs
			if not self.has_stairs:
				self.place_tile(self.exit_nodes[-1], 'Stairs')
				
			# We don't need anymore tiles, fill the rest with end pieces
			for n in self.exit_nodes:
				self.place_tile(n, 'Ends', check_collision=False)
		
	def check_dungeon(self):
		"""Checks to make sure the dungeon is up to spec"""
		return self.room_count > self.min_rooms and	self.has_stairs
		
	def place_tile(self, node, type, check_collision=True):
		scene = GameLogic.getCurrentScene()
	
		# Get the tile to place
		random.seed()
		index = random.randint(0, len(self.tiles[type]) - 1)
		tile = self.tiles[type][index]
		
		#print('\nAttempting to place %s...' % type)
		# First try to add the object; if it doesn't exist, merge the scene and try again
		# try:
		tile_node = scene.addObject(tile, node.object)
		# except ValueError:
			# GameLogic.LibLoad(self.blend, 'Scene', tile[1])
			# tile_node = scene.addObject(tile[0], node.object)
			
		# Get the mesh to use for collision detection
		for ob in tile_node.childrenRecursive:
			if ob.name.endswith('_tile'):
				tile_obj = ob
				break
				
		# Use the meshes to test for collision
		if (check_collision and self.check_collision(tile_obj, tile_obj.meshes)):
			# If our try limit has not been reached, try again
			tile_obj = None
			tile_node.endObject()	
			if self.tries < self.max_tries:
				#print('Collision! Trying again.')
				self.tries += 1
							
				self.use_as_next_node = node
			else:
				#print('Maximum tries reached, force an end')
				# The limit has been reached, force a dead end
				self.tries = 0
				self.place_tile(node, 'Ends', check_collision=False)
		else:
			# Success! Store some data and cleanup
			self.tries = 0
			#print('Tile placed!')
			# This node is done, remove it from the list
			self.exit_nodes.remove(node)
			
			# Collect nodes
			for ob in tile_node.childrenRecursive:
				if ob.name.startswith('exit'):
					if type == 'Doors':
						n_type = EN_DOOR
					elif type == 'Rooms':
						n_type = EN_ROOM
					else:
						n_type = EN_CORR
						
					self.exit_nodes.append(ExitNode(ob, n_type))
				elif ob.name.startswith('encounter'):
					self.encounter_nodes.append(ob)
					
			# See if anything needs to be done based on the type of tile placed
			if type == 'Rooms':
				self.room_count += 1
				tile_obj['encounter'] = True
			elif type == 'Stairs':
				self.has_stairs = True
			
			# Mathutils.Vector and Mathutils.Matrix can not be pickled, so convert them
			pos = [i for i in tile_node.worldPosition]
			ori = [[a, b, c] for a, b, c in tile_node.worldOrientation]
			
			# Add the tile name and position to the result list
			self.result.append((type, index, pos, ori))
			self.rooms[str(tile_obj.getPhysicsId())] = tile_obj
			self._tiles.append(BlenderWrapper.Object(tile_node))
				
	def check_collision(self, tile, meshes):
		# Iterate the verts
		for mesh in meshes:
			for mat in range(mesh.numMaterials):
				for v_index in range(mesh.getVertexArrayLength(mat)):
					vert = mesh.getVertex(mat, v_index)
					
					vert_pos = vert.getXYZ()[:]
					
					# Scale the vert_pos on the x and y a bit to account for slight overlaps (where the tiles connect)
					vert_pos[0] *= 0.9
					vert_pos[1] *= 0.9
					
					# Convert the vertex's local position to world space
					
					# This was the old way
					#from_pos = Vector(vert_pos) + Vector(tile.worldPosition)
					ori = tile.worldOrientation
					# The new way
					from_pos = (Matrix(ori[0], ori[1], ori[2]) * Vector(vert_pos)) + Vector(tile.worldPosition)

					
					# The to position is just x units below the vert
					to_pos = from_pos[:]
					to_pos[2] -= self.ray_length
					
					# Cast a ray from the vert down
					hit_tuple = tile.rayCast(to_pos, from_pos)

					if hit_tuple[0] and hit_tuple[0].name.endswith('_tile') and hit_tuple[0] != tile:
						# Collision!
						#print('Collision with %s and %s at %s' % (hit_tuple[0], tile, hit_tuple[1]))
						return True
						
		# Made it through, with no collision
		return False
		
# class EncounterDeck():
	# def __init__(self, deckfile):
		# self.Deckfile = deckfile
		# self.Deck = []
		# self.build_deck()
		
	# def build_deck(self):
		# deckfile = DeckFile(self.Deckfile)
		# toclose = []
		# for card in deckfile.root:
			# monster = None
			# role = ""
			# count = 0
			# for element in card:
				# if element.tag == "monster":
					# monster = element.text
				# if element.tag == "role":
					# role = element.text
				# elif element.tag == "count":
					# count = int(element.text)
			
			# for i in range(count):
				# self.Deck.append((monster, role))
				
		# deckfile.close()
				
	# def generate_encounter(self, num_players):
		# noBrutesSoldiers = True
		# while noBrutesSoldiers:
			# count = num_players
			# MonsterList = []
			# remove = []
			# while count > 0:		#while there are still players left with out cards
				# random.seed()
				# draw = random.choice(self.Deck)
				# while draw in MonsterList:				#If the card was already drawn, draw again
					# if len(remove) >= len(self.Deck):
						# self.build_deck()
					# draw = random.choice(self.Deck)
					
				# # see what we get and appropriately deal with the card
				# if draw[1] in ('soldier', 'brute'):
					# MonsterList.extend([draw[0] for i in range(2)])
					# remove.append(draw)
					# noBrutesSoldiers = False
				# elif draw[1] == 'minion':
					# MonsterList.extend([draw[0] for i in range(4)])
					# remove.append(draw)
				# elif draw[1] == 'lurker':
					# MonsterList.append(draw[0])
					# remove.append(draw)
					# count += 1
				# elif draw[1]:
					# MonsterList.append(draw[0])
					# remove.append(draw)
					# count -= 1
				# else:
					# MonsterList.append(draw[0])
					# remove.append(draw)
				# count -= 1
				
		# # Since we have a good encounter, remove the drawn cards from the deck
		# for draw in remove:
				# self.Deck.remove(draw)
		# return MonsterList
				
			
		
		