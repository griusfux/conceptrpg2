# $Id$

# Description: Wraps a KX_GameObject to be used with the system
# Contributers: Mitchell Stokes

# Movement modes
MOVE_LINV = 0
MOVE_FORCE = 1
MOV_LOC = 2
MOV_SERVO = 3
MOV_POS = 4

class BlenderObjectWrapper:
	"""KX_GameObject wrapper"""
	
	def __init__(self, gameobj):
		self.gameobj = gameobj
		try:
			self.armature = [i for i in gameobj.childrenRecursive if i.name == "KatArm"][0]
		except:
			self.armature = None
	def Move(self, vec, mode=MOVE_LINV, local=True):
		"""Do object movement"""
		
		if mode == MOVE_LINV:
			self.gameobj.setLinearVelocity(vec, local)
		elif mode == MOVE_FORCE:
			self.gameobj.applyForce(vec, local)
		elif mode == MOVE_LOC:
			self.gameobj.applyMovement(vec, local)
		elif mode == MOVE_SERVO:
			self.gameobj.applyForce(vec, local)
		elif mode == MOVE_POS:
			self.gameobj.position = vec
		else:
			raise ValueError("Supplied mode is invalid!")
			
	def GetPosition(self):
		return self.gameobj.worldPosition
		
	def SetPosition(self, position):
		self.gameobj.worldPosition = position
			
	def Rotate(self, vec, local=True):
		"""Do object rotation"""
		
		self.gameobj.applyRotation(vec, local)
		
	def PlayAnimation(self, anim):
		self.gameobj.sendMessage("animation", anim, self.armature.name)
		
	def GetVertexList(self):
		vertexList = []
		mesh = self.gameobj.meshes[0]
		
		for matID in range(mesh.numMaterials):
			length = mesh.getVertexArrayLength(matID)
			for array in range(0, length):
				vertexList.append(mesh.getVertex(matID, array))
				
		return [BlenderVertexWrapper(vertex, self.gameobj) for vertex in vertexList]
		
class BlenderVertexWrapper:
	def __init__(self, vertex, gameobj):
		self.x, self.y, self.z =  [gameobj.worldPosition[i] + vertex.getXYZ()[i] for i in range(3)]