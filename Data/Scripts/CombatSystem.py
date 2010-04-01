from Scripts.Ai.ai import ai
import random

TILE_SIZE	= 1
GRID_Z		= 0.1


class CombatSystem:
	def __init__(self, empty, Engine, encounter_list, room):
		random.seed()
		self.count = 5
		#Wrap all the enemies in an ai object
		self.enemy_list = [ai(enemy) for enemy in encounter_list]
		print([i.monster.name for i in self.enemy_list])
		
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
		self.origin = (smallestX, largestY, GRID_Z)
		
		# Uncomment for the debug marker
		empty.SetPosition(self.origin)
		self.debug_marker = Engine.AddObject('debug', empty, 0)
		
		#Generate the grid
		self.grid = CombatGrid(empty, Engine, self.origin, self.roomX, self.roomY)
		
		##################
		##Place Monsters##
		##################

		for monster in self.enemy_list:
			monster.x = random.randrange(0, grid.xSteps)
			monster.y = random.randrange(0, grid.ySteps)
			Engine.AddObject(monster.monster.id, empty, 0)
			tile = grid.map[monster.x][monster.y]
			monster.monster.object.SetPosition([tile.x, tile.y, GRID_Z])
			print([tile.x, tile.y, GRID_Z])
		
	def TileFromPoint(self, point):
		x_off = abs(point[0] - self.origin[0])
		y_off = abs(point[1] - self.origin[1])
		
		return self.grid(int(x_off/TILE_SIZE), int(y_off/TILE_SIZE))
		
	def Update(self, main):
		"""This function is called every frame to make up the combat loop"""
	
		self.debug_marker.SetPosition(self.TileFromPoint(main['player'].obj.GetPosition()).position)
	
		inputs = main['input_system'].Run()
		if inputs:
			if "Jump" in inputs:
				return False
		
			main['player'].PlayerPlzMoveNowzKThxBai(inputs, main['client'])
		else:
			main['player'].move_to_point(self.TileFromPoint(main['player'].obj.GetPosition()).position)
			
		return True		
		
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, empty, Engine, origin, roomX, roomY):
		# Position the main empty
		empty.SetPosition(origin)
		
		# Find out how many tiles need to be in the room
		self.xSteps = int(round(roomX / TILE_SIZE))
		self.ySteps = int(round(roomY / TILE_SIZE))
		
		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(self.ySteps)] for i in range(self.xSteps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(self.xSteps):
			yList = [None for i in range(self.ySteps)]
			for y in range (self.ySteps):
				empty.SetPosition((origin[0] + x, origin[1] - y, GRID_Z))
				self.map[x][y] = CombatTile(origin[0] + x, origin[1] - y, empty, Engine)
				
	def __call__(self, x, y):
		return self.map[x][y]
				
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, empty, Engine):
		self.x = x + TILE_SIZE / 2
		self.y = y - TILE_SIZE / 2
		self.position = (self.x, self.y, GRID_Z)#(self.x + TILE_SIZE / 2, self.y + TILE_SIZE / 2, GRID_Z)
		self.grid_tile = Engine.AddObject('GridTile', empty, 0)
		self.grid_color = Engine.AddObject('GridColor', empty, 0)