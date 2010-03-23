from Scripts.Ai.ai import ai
import GameLogic as gl
TILE_SIZE	= 1
GRID_Z		= 0.01


class CombatSystem:
	def __init__(self, empty, Engine, encounter_list, room):
		##variables
		#enemy_list
		#roomX
		#roomY
		self.count = 5
		#Wrap all the enemies in an ai object
		self.enemy_list = [ai(enemy) for enemy in encounter_list]
		print([i.monster.name for i in self.enemy_list])
		
		#Survey the room

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
		
		empty.SetPosition(self.origin)
		gl.getCurrentScene().addObject('debug', empty.gameobj, 0)
		#Generate the grid
		grid = CombatGrid(empty, Engine, self.origin, self.roomX, self.roomY)\
		
	def Update(self):
		"""This function is called every frame to make up the combat loop"""
	
		self.count -= 1
		if self.count <= 0:
			return False
		
		return True
		
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	def __init__(self, empty, Engine, origin, roomX, roomY):
		# Position the main empty
		empty.SetPosition(origin)
		
		# Find out how many tiles need to be in the room
		xSteps = int(roomX // TILE_SIZE)
		ySteps = int(roomY // TILE_SIZE)
		
		# Create an empty 2D list to hold the grid
		self.map = [[None for i in range(ySteps)] for i in range(xSteps)]
		
		# Fill the 2D grid list with CombatTile objects
		for x in range(xSteps):
			yList = [None for i in range(ySteps)]
			for y in range (ySteps):
				empty.SetPosition((origin[0] + x, origin[1] - y, GRID_Z))
				self.map[x][y] = CombatTile(x, y, empty, Engine)
				
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	def __init__(self, x, y, empty, Engine):
		self.x = x
		self.y = y
		self.position = (self.x + TILE_SIZE / 2, self.y + TILE_SIZE / 2, GRID_Z)
		self.grid_tile = Engine.AddObject('GridTile', empty, 0)
		self.grid_color = Engine.AddObject('GridColor', empty, 0)