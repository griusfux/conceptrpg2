from Scripts.Ai.ai import ai
import random

# Grid constants
TILE_SIZE	= 1
GRID_Z		= 0.1

class CombatSystem:
	def __init__(self, main, Engine, encounter_list, room):
		self.main = main.gameobj
		random.seed()
		#Wrap all the enemies in an ai object
		self.enemy_list = [ai(enemy) for enemy in encounter_list]
		
		###################
		##Survey the room##
		###################

		vertList = [i for i in room.GetVertexList() if i.z <= 0]
		
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
		
		#Generate the grid
		self.grid = CombatGrid(main, Engine, self.origin, self.roomX, self.roomY)
			
		# Make sure the player is in the room
		self.main['player'].move_to_point(self.tile_from_point(self.main, self.main['player'].obj.GetPosition()).position)

		# Place the monsters

		for monster in self.enemy_list:
			monster.x = random.randrange(0, self.grid.xSteps)
			monster.y = random.randrange(0, self.grid.ySteps)
			Engine.AddObject(monster.monster.id, main, 0)
			tile = self.grid.map[monster.x][monster.y]
			monster.monster.object.SetPosition(tile.position)
			
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
			main['player'].obj.SetPosition(tile.position)
			
		return tile
		
	def update(self, main):
		"""This function is called every frame to make up the combat loop"""

		# self.debug_marker.SetPosition(self.tile_from_point(main, main['player'].obj.GetPosition()).position)
	
		inputs = main['input_system'].Run()
		if inputs:
			if "Jump" in inputs:
				return False
		
			main['player'].PlayerPlzMoveNowzKThxBai(inputs, main['client'])
		else:
			main['player'].move_to_point(self.tile_from_point(main, main['player'].obj.GetPosition()).position)
			
		return True		
		
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, empty, Engine, origin, roomX, roomY):
		# Position the main empty
		empty.SetPosition(origin)
		
		# Find out how many tiles need to be in the room
		self.xSteps = int(round(roomX / TILE_SIZE)) + 2 * TILE_SIZE
		self.ySteps = int(round(roomY / TILE_SIZE)) + 2 * TILE_SIZE
		
		print(self.xSteps, self.ySteps)
		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(self.ySteps)] for i in range(self.xSteps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(self.xSteps):
			for y in range(self.ySteps):
				empty.SetPosition((origin[0] + x, origin[1] - y, GRID_Z))
				self.map[x][y] = CombatTile(x, y, [origin[0] + x, origin[1] - y], empty, Engine, self.xSteps, self.ySteps)
	
	def __del__(self):
		for x in self.map:
			for y in x:
				del y
				
	def __call__(self, x, y):
		return self.map[x][y]
				
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, position, empty, Engine, xSteps, ySteps):
		self.x = x
		self.y = y
		self.position = ((position[0] + TILE_SIZE / 2) + 1, position[1] - TILE_SIZE / 2, GRID_Z)
		self.valid = True
		
		self.grid_color = Engine.AddObject('GridColor', empty, 0)
		self.grid_color.set_color([0, 0, 0, 0])
		
		if self.x in (0, xSteps - 1) or self.y in (0, ySteps - 1):
			self.valid = False
			
		if self.valid:
			self.grid_tile = Engine.AddObject('GridTile', empty, 0)
		else:
			self.grid_tile = Engine.AddObject('GridInvalid', empty, 0)
			self.grid_color.set_color([1, 0, 0, 1])
		
	def __del__(self):
		self.grid_tile.End()
		self.grid_color.End()