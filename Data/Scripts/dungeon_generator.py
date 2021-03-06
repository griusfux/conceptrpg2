# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
import GameLogic
import Scripts.blender_wrapper as BlenderWrapper
from mathutils import Vector, Matrix
from Scripts.packages import EncounterDeck

import math

GEN_LINEAR = 0
GEN_RANDOM = 1

BIAS = 0.1

# ExitNode types
EN_ROOM = 0
EN_CORR = 1
EN_DOOR = 2

class ExitNode:
	"""A class to store exit node information"""
	
	def __init__(self, obj, type):
		self.object = obj
		self.type = type
		
class ShopNode:
	"""A class to store shop node information"""
	
	def __init__(self, pos, ori):
		self.position = pos
		self.orientation = ori

class DungeonGenerator:
	"""A class for generating dungeons"""
	
	# Some settings
	max_rooms = 10
	min_rooms = 8
	max_tries = 5
	ray_length = 5
	dead_end_thresh = 0.5
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
				'Barriers': [i['obj'] for i in map.combat_barriers],
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
		
		# Keep track of dead-ends so we can potenially clean some up
		self._dead_ends = []
		
		# This is used so we can clear the dungeon if we need to
		self._tiles = []
		
		# Where to place the shop keeper
		self.shop_node = None
	
	def generate_from_list(self, main, result):
		"""Use a result list to generate the dungeon"""	
		
		self.clear()
		
		for type, index, room_id, position, ori in result:
			if type == "Shop":
				self.shop_node = ShopNode(position, ori)
			else:
				tile = self.tiles[type][index]

				tile_node = main['engine'].add_object(tile, position, ori)
					
				# Get the mesh
				for ob in tile_node.gameobj.childrenRecursive:
					if ob.name.endswith('_tile'):
						tile_obj = ob
						break
				else:
					raise ValueError("No tile found for "+tile_node.name)
				
				if type == "Rooms":
					self.room_count += 1
					self.rooms[str(room_id)] = BlenderWrapper.Object(tile_obj)
					tile_obj['room_id'] = room_id
					tile_obj['encounter'] = True
				elif type == "Stairs":
					self.has_stairs = True
					
				self._tiles.append(tile_node)
				
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
		
		self.start_position = self._tiles[0].position
		
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
					if not self.has_stairs: tile = 'Stairs'
					else: tile = 'Corridors'
				elif roll < 20 and roll >= 9:
					tile = 'Rooms'
				else:
					tile = 'Corridors'	
			else:
				if roll == 20:
					tile = 'Ends'
				elif roll == 19:
					if not self.has_stairs: tile = 'Stairs'
					else: tile = 'Corridors'
				elif roll < 19 and roll >= 10:
					tile = 'Rooms'
#				elif roll <13 and roll >= 10:
#					tile = 'Rooms'
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
		else:
			raise ValueError("No tile found for "+tile_node.name)
				
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
				
				# But, first check if there is another dead end close enough
				if (self.clean_dead_ends(node.object)):
					self.tries = 0
					self.exit_nodes.remove(node)
					return
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
				elif ob.name.startswith('shop'):
					pos = [i for i in ob.worldPosition]
					ori = [[a, b, c] for a, b, c in ob.worldOrientation]
					self.result.append(("Shop", 0, 0, pos, ori))
					
					self.shop_node = ShopNode(pos, ori)
				elif 'volume' in ob and ob['volume'] == "encounter":
					ob['encounter'] = True
					ob['room_id'] = self.room_count+1
					
			# See if anything needs to be done based on the type of tile placed
			if type == 'Rooms':
				self.room_count += 1
				self.rooms[str(self.room_count)] = BlenderWrapper.Object(tile_obj)
				tile_obj['room_id'] = self.room_count
			elif type == 'Stairs':
				self.has_stairs = True
			elif type == 'Ends':
				self._dead_ends.append(tile_node)
			
			# Mathutils.Vector and Mathutils.Matrix can not be pickled, so convert them
			pos = [i for i in tile_node.worldPosition]
			ori = [[a, b, c] for a, b, c in tile_node.worldOrientation]
			
			# Add the tile name and position to the result list
			self.result.append((type, index, self.room_count, pos, ori))
			self._tiles.append(BlenderWrapper.Object(tile_node))
				
	def clean_dead_ends(self, node_object):
		a = node_object.worldPosition
	
		for ob in self._dead_ends:
			b = ob.worldPosition
			
			if abs(a[0]-b[0]) < self.dead_end_thresh and \
				abs(a[1]-b[1]) < self.dead_end_thresh and \
				abs(a[2]-b[2]) < self.dead_end_thresh:
				self._dead_ends.remove(ob)
				ob.endObject()
				return True
				
		return False
			
	def check_collision(self, tile, meshes):
		# Iterate the verts
		for mesh in meshes:
			for mat in range(mesh.numMaterials):
				for v_index in range(mesh.getVertexArrayLength(mat)):
					vert = mesh.getVertex(mat, v_index)
					
					vert_pos = vert.getXYZ().copy()
					
					# Scale the vert_pos on the x and y a bit to account for slight overlaps (where the tiles connect)
					vert_pos[0] *= 1-BIAS
					vert_pos[1] *= 1-BIAS
					
					# Convert the vertex's local position to world space
					
					# This was the old way
					#from_pos = Vector(vert_pos) + Vector(tile.worldPosition)
					ori = tile.worldOrientation
					# The new way
					from_pos = (Matrix(ori) * Vector(vert_pos)) + Vector(tile.worldPosition)

					
					# The to position is just x units below the vert
					to_pos = from_pos.copy()
					to_pos[2] -= self.ray_length
					
					# Cast a ray from the vert down
					hit_tuple = tile.rayCast(to_pos, from_pos)

					if hit_tuple[0] and hit_tuple[0].name.endswith('_tile') and hit_tuple[0] != tile:
						# Collision!
						# print('Collision with %s and %s at %s' % (hit_tuple[0], tile, hit_tuple[1]))
						return True
						
		# Made it through, with no collision
		return False
	
	def get_id_from_message(self, mess):
		"""Gets a room_id from a Message sensor"""
		
		room_id = None
		
		if mess.positive:
			room_id = mess.bodies[0]
			
		return room_id
	
	def clear_encounter(self, room):
		"""Clears the encounter volume from the given room"""
		
		room = room.gameobj
		
		for ob in room.childrenRecursive:
			if 'volume' in ob and ob['volume'] == "encounter":
				ob.endObject()
			if ob.name == self.tiles['Barriers'][0]:
				ob.endObject()
				
	def clear_barriers(self, room):
		"""Clear just the barriers instead of the whole encounter (used for player death)"""
		
		room = room.gameobj
		
		for ob in room.childrenRecursive:
			if ob.name == self.tiles['Barriers'][0]:
				ob.endObject()
		
	def place_combat_barriers(self, room):
		"""Places combat barriers at the entrance and exits"""
		
		scene = GameLogic.getCurrentScene()
		barrier = self.tiles['Barriers'][0]
		room = room.gameobj
		
		# Entrance
		newob = scene.addObject(barrier, room.parent)
		newob.setParent(room, True, False)
		
		# Exits
		for ob in [i for i in room.parent.childrenRecursive if i.name.startswith('exit')]:
			newob = scene.addObject(barrier, ob)
			
			# We need to rotate PI radians about the z axis since the exits are facing the other way
			rot_mat = Matrix.Rotation(math.pi, 3, 'Z')
			newob.localOrientation = newob.localOrientation * rot_mat
			
			newob.setParent(room, True, False)

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
				
			
		
		