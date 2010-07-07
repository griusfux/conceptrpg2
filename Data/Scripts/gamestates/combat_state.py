# $Id$

import Scripts.Ai.machine as ai
import random
from math import sqrt


# Grid constants
TILE_SIZE	= 1
GRID_Z		= 0.01

class CombatState:
	def __init__(self, main, Engine, encounter_list, room):
		random.seed()
		self.Engine = Engine
		###################
		# Prepare Enemies
		
		print("Monsters in this encounter:")
		[print(('\t%s' % i.name)) for i in encounter_list]
		self.enemy_list = []
		# Add an ai fsm to each monster based on their ai keywords
		for enemy in encounter_list:
			enemy.ai = ai.Machine(enemy.ai_keywords, enemy.ai_start_state)
			self.enemy_list.append(enemy)
			
		###################
		# Setup the room

		vert_list = [i for i in room.get_vertex_list() if i.z <= 0]
		self.room = CombatRoom(vert_list, room)
			
		#Generate the grid
		self.grid = CombatGrid(Engine, self.room)
			
			# Uncomment and dedent for the debug marker
			# main.SetPosition(self.origin)
			# self.debug_marker = Engine.AddObject('debug', main, 0)

		######################
		# Place participants
		
		# Make sure the player is in the room
		main['player'].obj.set_position(self.tile_from_point(main['player'].obj.get_position()).position)

		# Place the monsters

		for monster in self.enemy_list:
			while True:
				monster.x = random.randrange(0, self.grid.x_steps)
				monster.y = random.randrange(0, self.grid.y_steps)
				if self.grid(monster.x, monster.y).valid:
					break
			tile = self.grid.map[monster.x][monster.y]
			monster.obj = Engine.add_object(monster.id, tile.position)
			tile.fill(monster)
			monster.target = None
		
	def update(self, main):
		"""This function is called every frame to make up the combat loop"""
		
		# Clear the color of the tiles
		for row in self.grid.map:
			for tile in row:	
				tile.color((0, 0, 0, 0))
		
		# Establish the input dictionary for the ai
		machine_input = {
						'self'		: 'Set when ai is run',
						'foe_list'	: (main['player'],)
						}
						
		# Run the enemy ai
		for enemy in self.enemy_list:
			machine_input['self'] = enemy
			enemy.ai.run(machine_input)

		# self.debug_marker.SetPosition(self.tile_from_point(main, main['player'].obj.GetPosition()).position)
		
		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].obj.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handle inputs
		inputs = main['input_system'].run()
		# if set(["MoveForward", "MoveBackward", "TurnLeft", "TurnRight", "Jump", "Aim"]).intersection(set(inputs)):
		if inputs:
			if set([("MoveForward", "INPUT_ACTIVE"), ("MoveBackward", "INPUT_ACTIVE"), ("MoveLeft", "INPUT_ACTIVE"), ("MoveRight", "INPUT_ACTIVE")]).intersection(set(inputs)) and not main['player'].lock:
				main['player'].move_player(inputs, main['input_system'].mouse, main['client'])
			else:
				# Snap the player to the grid
				target_tile = self.tile_from_point(main['player'].obj.get_position())
				vector_to_tile = main['player'].obj.get_local_vector_to(target_tile.position)
				vector_to_tile[2] = 0
				vector_to_tile = [component*main['player'].speed for component in vector_to_tile]
				main['player'].obj.move(vector_to_tile)
				
			if not main['player'].lock:
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].active_power.use(self, main['player'], target)
			
			
				if ("Jump", "INPUT_ACTIVE") in inputs:
					return False
				if ("Aim", "INPUT_ACTIVE") in inputs:
					self.display_target_range('area burst 5', main['player'].obj.get_position())

				
		else:
			pass		
				
		return True	
		

	def play_animation(self, char, action):
		char.obj.play_animation(action)
		
	def end(self):
		self.grid.end()
		
		for enemy in self.enemy_list:
			enemy.obj.end()
		
################################################################################
# Utility Functions
#		
	def tile_from_point(self, point):
		# Calculate the offset based on the distance from the origin
		x_off = abs(point[0] - self.room.origin[0])
		y_off = abs(point[1] - self.room.origin[1])
		
		# Convert the offset to tiles
		x = int(x_off/TILE_SIZE)
		y = int(y_off/TILE_SIZE)
		
		# Clamp the player's position to be within the grid
		out_of_bounds = False
		
		if x > self.grid.x_steps - 1:
			x = self.grid.x_steps - 1
		elif x < 0:
			x = 0
			
		if y > self.grid.y_steps - 1:
			y = self.grid.y_steps - 1 
		elif y < 1:
			y = 1
		
		tile = self.grid(x, y)
		# force the player to be inside the bounds
		# if out_of_bounds:
			# main['player'].obj.set_position(tile.position)
			
		return tile
	
	def find_target_range(self, target_range, point):
		target_range = target_range.strip().split(' ')
		point = (point[0], point[1], point[2])
		if target_range[0] == 'melee':
			tiles = []
			for i in range(int(target_range[1])):
				# if x+:
				tiles.append(self.tile_from_point((point[0]+TILE_SIZE*(i+1), point[1])))
				# elif x-:
				tiles.append(self.tile_from_point((point[0]-TILE_SIZE*(i+1), point[1])))
				# elif y+:
				tiles.append(self.tile_from_point((point[0], point[1]+TILE_SIZE*(i+1))))
				# elif y-:
				tiles.append(self.tile_from_point((point[0], point[1]-TILE_SIZE*(i+1))))
		elif target_range[0] == 'ranged':
			if target_range[1] == 'weapon':
				pass
			elif target_range[1] == 'sight':
				pass
			else: # It's a number
				pass
		elif target_range[0] == 'close':
			if target_range[1] == 'burst':
				pass
			elif target_range[1] == 'blast':
				pass
			else:
				print("Invalid argument for 'close' range: %s" % target_range[1])
		elif target_range[0] == 'area':
			if target_range[1] == 'burst':
				tiles = []
				radius = int(target_range[2])+1
				y_vals = [sqrt((radius**2) - ((i+0.5)**2)) for i in range(radius)]
				for x in range(int(target_range[2])+1):
					for y in range(int(round(y_vals[x]))):
						tiles.append(self.tile_from_point((point[0]+x*TILE_SIZE, point[1] + y*TILE_SIZE)))
				point = self.tile_from_point(point)
				next_quarter = [self.grid(curr.x - (curr.x-point.x)*2, curr.y) for curr in tiles if curr]
				tiles += next_quarter
				next_half = [self.grid(curr.x, curr.y - (curr.y-point.y)*2) for curr in tiles if curr]
				tiles += next_half
			elif target_range[1] == 'wall':
				pass
			else:
				print("Invalid argument for 'area' range: %s" % target_range[1])
		else:
			print("Invalid range type: %s" % target_range[0])

		# Remove invalid tiles
		while None in tiles:
			tiles.remove(None)
		return tiles
		
		
	def display_target_range(self, target_range, point, display='neutral'):
		colors = {
			'neutral' :	[1, 0, 0, .8] }
		tiles = self.find_target_range(target_range, point)
		for tile in tiles:
				if tile.valid:
					tile.color(colors[display])
			
################################################################################
# Combat Objects
#
class CombatRoom:
	"""This object holds the room data"""
	def __init__(self, vert_list, obj):
		self.object = obj
		smallestX = vert_list[0].x
		smallestY = vert_list[0].y
		largestX = vert_list[0].x
		largestY = vert_list[0].y
		
		for vertex in vert_list:
			if vertex.x < smallestX:
				smallestX = vertex.x
			elif vertex.x > largestX:
				largestX = vertex.x

			if vertex.y < smallestY:
				smallestY = vertex.y
			elif vertex.y > largestY:
				largestY = vertex.y
		
		self.x = largestX - smallestX
		self.y = largestY - smallestY
		self.origin = (smallestX, largestY, GRID_Z) # For padding - TILE_SIZE from x and + TILE_SIZE for y
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, Engine, room):		
		# Find out how many tiles need to be in the room
		self.x_steps = int(round(room.x / TILE_SIZE)) # + 2 * TILE_SIZE #for padding
		self.y_steps = int(round(room.y / TILE_SIZE)) # + 2 * TILE_SIZE #for padding

		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(self.y_steps)] for i in range(self.x_steps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(self.x_steps):
			for y in range(self.y_steps):
				# position =(room.origin[0] + x, room.origin[1] - y, GRID_Z)
				self.map[x][y] = CombatTile(x, y, (room.origin[0] + x, room.origin[1] - y, GRID_Z), Engine, room, self.x_steps, self.y_steps)
	
	def end(self):
		for x in self.map:
			for y in x:
				y.end()
				
	def __call__(self, x, y):
		# Make sure the coordinates are positive, or python will access the grid backwards
		if x < 0 or y < 0:	
			return None
			
		# Make sure the tile is in range
		try:
			return self.map[x][y]
		except IndexError:
			return None
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, position, Engine, room, x_steps, y_steps):
		self.x = x
		self.y = y
		self.position = ((position[0] + TILE_SIZE / 2), position[1] - TILE_SIZE / 2, position[2])
		self.valid = True
		self.obj = None
		
		self.grid_color = Engine.add_object('GridColor', position)
		self.grid_color.set_color([0, 0, 0, 0])
		
		# Check if we're out side the room or on the border
		# if self.x in (0, x_steps - 1) or self.y in (0, y_steps - 1):
			# self.valid = False
		# else:
		for vert in self.grid_color.get_vertex_list():
			hit_ob, hit_pos, hit_norm = Engine.ray_cast((vert.x, vert.y, vert.z + 1), (vert.x, vert.y, vert.z-1), self.grid_color, 'encounter')
			if not hit_ob or hit_ob.gameobj != room.object.gameobj:
				# We didn't find the room, don't bother with the rest of the verts
				self.valid = False
				break
					
		# Check if anything is in the tile
		v1 = self.grid_color.get_vertex_list()[0]
		v2 = self.grid_color.get_vertex_list()[2]
		hit_ob, hit_pos, hit_norm = Engine.ray_cast((v1.x, v1.y, v1.z), (v2.x, v2.y, v2.z), self.grid_color)
		if hit_ob:
			self.valid = False
			
		# Place the appropriate tile based on validity
		if self.valid:
			self.grid_tile = Engine.add_object('GridTile', position)
		else:
			self.grid_tile = None #Engine.add_object('GridInvalid', position)
	
	def color(self, color):
		self.grid_color.set_color(color)
		
	def fill(self, obj):
		self.obj = obj
		self.valid = False
		
	def end(self):
		self.grid_tile.end()
		self.grid_color.end()