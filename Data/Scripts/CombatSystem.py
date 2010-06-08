# $Id$

from Scripts.Ai.ai import ai
import random

# Grid constants
TILE_SIZE	= 1
GRID_Z		= 0.1

class CombatSystem:
	def __init__(self, main, empty, Engine, encounter_list, room):
		random.seed()
		
		print([i.name for i in encounter_list])
		#Wrap all the enemies in an ai object
		self.enemy_list = [ai(enemy) for enemy in encounter_list]
		
		###################
		##Survey the room##
		###################

		vertList = [i for i in room.get_vertex_list() if i.z <= 0]
		
		smallestX = vertList[0].x
		smallestY = vertList[0].y
		largestX = vertList[0].x
		largestY = vertList[0].y
		
		for vertex in vertList:
			if vertex.x < smallestX:
				smallestX = vertex.x
			elif vertex.x > largestX:
				largestX = vertex.x

			if vertex.y < smallestY:
				smallestY = vertex.y
			elif vertex.y > largestY:
				largestY = vertex.y
		
		self.roomX = largestX - smallestX
		self.roomY = largestY - smallestY
		self.origin = (smallestX - TILE_SIZE, largestY + TILE_SIZE, GRID_Z)
	
		# Uncomment for the debug marker
		# main.SetPosition(self.origin)
		# self.debug_marker = Engine.AddObject('debug', main, 0)
		
		# Move the player out of the way
		
		#Generate the grid
		self.grid = CombatGrid(empty, Engine, self.origin, room, self.roomX, self.roomY)
			
		# Make sure the player is in the room
		main['player'].move_to_point(self.tile_from_point(main, main['player'].obj.get_position()).position)

		# Place the monsters

		for monster in self.enemy_list:
			while True:
				monster.x = random.randrange(0, self.grid.xSteps)
				monster.y = random.randrange(0, self.grid.ySteps)
				
				if self.grid(monster.x, monster.y).valid:
					break
			Engine.add_object(monster.monster.id, empty, 0)
			tile = self.grid.map[monster.x][monster.y]
			monster.monster.object.set_position(tile.position)
			
	def __del__(self):
		del self.grid
		
		for enemy in self.enemy_list:
			del enemy
		
	def tile_from_point(self, main, point):
		# Calculate the offset based on the distance from the origin
		x_off = abs(point[0] - self.origin[0])
		y_off = abs(point[1] - self.origin[1])
		
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
		
	def update(self, main):
		"""This function is called every frame to make up the combat loop"""

		# self.debug_marker.SetPosition(self.tile_from_point(main, main['player'].obj.GetPosition()).position)
	
		inputs = main['input_system'].run()
		if set(["MoveForward", "MoveBackward", "TurnLeft", "TurnRight", "Jump"]).intersection(set(inputs)):
			if "Jump" in inputs:
				return False
		
			main['player'].move_player(inputs, main['input_system'].mouse, main['client'], None)
		else:
			main['player'].move_to_point(self.tile_from_point(main, main['player'].obj.get_position()).position)
			
		return True		
		
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, empty, Engine, origin, room, roomX, roomY):
		# Position the main empty
		empty.set_position(origin)
		
		# Find out how many tiles need to be in the room
		self.xSteps = int(round(roomX / TILE_SIZE)) + 2 * TILE_SIZE
		self.ySteps = int(round(roomY / TILE_SIZE)) + 2 * TILE_SIZE

		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(self.ySteps)] for i in range(self.xSteps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(self.xSteps):
			for y in range(self.ySteps):
				empty.set_position((origin[0] + x, origin[1] - y, GRID_Z))
				self.map[x][y] = CombatTile(x, y, [origin[0] + x, origin[1] - y], empty, Engine, room, self.xSteps, self.ySteps)
	
	def __del__(self):
		for x in self.map:
			for y in x:
				del y
				
	def __call__(self, x, y):
		return self.map[x][y]
				
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, position, empty, Engine, room, xSteps, ySteps):
		self.x = x
		self.y = y
		self.position = ((position[0] + TILE_SIZE / 2) + 1, position[1] - TILE_SIZE / 2, GRID_Z)
		self.valid = True
		
		self.grid_color = Engine.add_object('GridColor', empty, 0)
		self.grid_color.set_color([0, 0, 0, 0])
		
		# Check if we're out side the room or on the border
		if self.x in (0, xSteps - 1) or self.y in (0, ySteps - 1):
			self.valid = False
		else:
			for vert in self.grid_color.get_vertex_list():
				hit_ob, hit_pos, hit_norm = Engine.ray_cast((vert.x, vert.y, vert.z + 1), (vert.x, vert.y, vert.z-1), self.grid_color, 'encounter')
				if not hit_ob or hit_ob.gameobj != room.gameobj:
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
			self.grid_tile = Engine.add_object('GridTile', empty, 0)
		else:
			self.grid_tile = Engine.add_object('GridInvalid', empty, 0)
		
	def __del__(self):
		self.grid_tile.end()
		self.grid_color.end()