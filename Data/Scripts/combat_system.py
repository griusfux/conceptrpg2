# $Id $

import Scripts.Ai.machine as ai
import random


# Grid constants
TILE_SIZE	= 1
GRID_Z		= 0.1

class CombatSystem:
	def __init__(self, main, empty, Engine, encounter_list, room):
		random.seed()
		
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
		main['player'].move_to_point(self.tile_from_point(main, main['player'].obj.get_position()).position)

		# Place the monsters

		for monster in self.enemy_list:
			while True:
				monster.x = random.randrange(0, self.grid.xSteps)
				monster.y = random.randrange(0, self.grid.ySteps)
				
				if self.grid(monster.x, monster.y).valid:
					break
			tile = self.grid.map[monster.x][monster.y]
			monster.obj = Engine.add_object(monster.id, tile.position)
			tile.fill(monster)
		
	def update(self, main):
		"""This function is called every frame to make up the combat loop"""
		
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
	
		inputs = main['input_system'].run()
		if set(["MoveForward", "MoveBackward", "TurnLeft", "TurnRight", "Jump"]).intersection(set(inputs)):
			if "Jump" in inputs:
				return False

			main['player'].move_player(inputs, main['input_system'].mouse, main['client'])
		else:
			main['player'].move_to_point(self.tile_from_point(main, main['player'].obj.get_position()).position)
			
		return True		
		
	def __del__(self):
		del self.grid
		
		for enemy in self.enemy_list:
			enemy.obj.end()
		
################################################################################
# Utility Functions
#		
	def tile_from_point(self, main, point):
		# Calculate the offset based on the distance from the origin
		x_off = abs(point[0] - self.room.origin[0])
		y_off = abs(point[1] - self.room.origin[1])
		
		# Convert the offset to tiles
		x = int(x_off/TILE_SIZE) - 1
		y = int(y_off/TILE_SIZE)
		
		# Clamp the player's position to be within the grid
		out_of_bounds = False
		
		if x > self.grid.xSteps - 2:
			x = self.grid.xSteps - 2
			out_of_bounds = True
		elif x < 0:
			x = 0
			out_of_bounds = True
			
		if y > self.grid.ySteps - 2:
			y = self.grid.ySteps - 2
			out_of_bounds = True
		elif y < 1:
			y = 1
			out_of_bounds = True
			
		tile = self.grid(x, y)
		
		# force the player to be inside the bounds
		if out_of_bounds:
			main['player'].obj.set_position(tile.position)
			
		return tile
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
		self.origin = (smallestX - TILE_SIZE, largestY + TILE_SIZE, GRID_Z)
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, Engine, room):		
		# Find out how many tiles need to be in the room
		self.xSteps = int(round(room.x / TILE_SIZE)) + 2 * TILE_SIZE
		self.ySteps = int(round(room.y / TILE_SIZE)) + 2 * TILE_SIZE

		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(self.ySteps)] for i in range(self.xSteps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(self.xSteps):
			for y in range(self.ySteps):
				# position =(room.origin[0] + x, room.origin[1] - y, GRID_Z)
				self.map[x][y] = CombatTile(x, y, [room.origin[0] + x, room.origin[1] - y, GRID_Z], Engine, room, self.xSteps, self.ySteps)
	
	def __del__(self):
		for x in self.map:
			for y in x:
				del y
				
	def __call__(self, x, y):
		return self.map[x][y]
				
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, position, Engine, room, xSteps, ySteps):
		self.x = x
		self.y = y
		self.position = ((position[0] + TILE_SIZE / 2) + 1, position[1] - TILE_SIZE / 2, position[2])
		self.valid = True
		self.obj = None
		
		self.grid_color = Engine.add_object('GridColor', position)
		self.grid_color.set_color([0, 0, 0, 0])
		
		# Check if we're out side the room or on the border
		if self.x in (0, xSteps - 1) or self.y in (0, ySteps - 1):
			self.valid = False
		else:
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
			self.grid_tile = Engine.add_object('GridInvalid', position)
			
	def fill(self, obj):
		self.obj = obj
		self.valid = False
		
	def __del__(self):
		self.grid_tile.end()
		self.grid_color.end()