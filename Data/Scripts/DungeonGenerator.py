import random
import GameLogic

GEN_LINEAR = 0
GEN_RANDOM = 1

# ExitNode types
EN_ROOM = 0
EN_CORR = 1
EN_DOOR = 2

class ExitNode:
	"""A class to store exit node information"""
	
	object = None
	type = 0

class DungeonGenerator:
	"""A class for generating dungeons"""
	
	# Some settings
	max_rooms = 10
	generation = GEN_RANDOM
	
	def __init__(self, mapfile):
		# Create some lists to store tiles
		# The lists are a list of tuples [(obj, scene)]
		
		self.tiles = {}
		
		self.tiles['Starts'] = []
		self.tiles['Rooms'] = []
		self.tiles['Corridors'] = []
		self.tiles['Ends'] = []
		self.tiles['Doors'] = []
		self.tiles['Stairs'] = []
		self.tiles['Traps'] = []
		
		# The list of exit nodes
		self.exit_nodes = []
		
		# The list of encounter nodes
		self.encounter_nodes = []
		
		# The current room count
		self.room_count = 0
		
		# Some flags for the currently placed tiles
		self.has_start = False
		self.has_stairs = False
		
		# Store the KX_Scene object
		self.scene = GameLogic.getCurrentScene()
	
		# Parse the xml file and fill the lists
		for element in mapfile.Root.iter():
			if element.tag == "start_tile":
				self.tiles['Starts'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "room_tile":
				self.tiles['Rooms'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "corridor_tile":
				self.tiles['Corridors'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "end_tile":
				self.tiles['Ends'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "door_tile":
				self.tiles['Doors'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "stair_tile":
				self.tiles['Stairs'].append((element.get("blend_obj"), element.get("blend_scene")))
			if element.tag == "trap_tile":
				self.tiles['Traps'].append((element.get("blend_obj"), element.get("blend_scene")))
	
	def HasNext(self):
		"""Check to see if there are still more exit nodes to fill"""
		return True if self.exit_nodes else False
		
	def GenerateFirst(self, node):
		"""Generate the first tile"""
		
		# Place the start tile
		self.PlaceTile(node, 'Starts')
		
	def GenerateNext(self):
		"""Generate the next tile"""
		
		random.seed()

		# Check to see if we should keep expanding the dungeon
		if self.room_count <= self.max_rooms:
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
				elif roll < 18 and roll >= 16:
					tile = 'Rooms'
				elif roll <16 and roll >= 13:
					tile = 'Doors'
				else:
					tile = 'Corridors'
			
			self.PlaceTile(node, tile)
		else:
			# We are done placing tiles
			
			# Check if we have some stairs
			if not self.has_stairs:
				self.PlaceTile(self.exit_nodes[-1], 'Stairs')
				
			# We don't need anymore tiles, fill the rest with end pieces
			for node in self.exit_nodes:
				self.PlaceTile(node, 'Ends')
		
	def PlaceTile(self, node, type):
		# Get the tile to place
		random.seed()
		index = random.randint(0, len(self.tiles[type]) - 1)
		tile = self.tiles[type][index]
		
		# First try to add the object; if it doesn't exist, merge the scene and try again
		GameLogic.LibLoad('
		tile_obj = scene.addObject(tile[0], node.object)
		