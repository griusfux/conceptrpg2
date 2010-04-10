# $Id$

# Description: Wraps a KX_GameObject to be used with the system
# Contributers: Mitchell Stokes

from Mathutils import Matrix, Vector
import GameLogic as gl

# Movement modes
MOVE_LINV = 0
MOVE_FORCE = 1
MOV_LOC = 2
MOV_SERVO = 3
MOV_POS = 4

class Object:
	"""KX_GameObject wrapper"""
	
	def __init__(self, gameobj):
		self.gameobj = gameobj
		armature = [i for i in gameobj.childrenRecursive if i.name == "KatArm"]
		if armature: self.armature = armature[0]
		
	def move(self, vec, mode=MOVE_LINV, local=True):
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
			
	def get_position(self):
		return self.gameobj.worldPosition
		
	def get_orientation(self):
		return self.gameobj.worldOrientation
		
	def set_position(self, position):
		self.gameobj.worldPosition = position[:]
		
	def set_orientation(self, ori):
		self.gameobj.worldOrientation = ori[:]
			
	def rotate(self, vec, local=True):
		"""Do object rotation"""
		
		self.gameobj.applyRotation(vec, local)
		
	def play_animation(self, anim):
		if self.armature:
			self.gameobj.sendMessage("animation", anim, self.armature.name)
			
	def end(self):
		self.gameobj.endObject()
		
	def get_vertex_list(self):
		vertexList = []
		mesh = self.gameobj.meshes[0]
		
		for matID in range(mesh.numMaterials):
			length = mesh.getVertexArrayLength(matID)
			for array in range(0, length):
				vertexList.append(mesh.getVertex(matID, array))
				
		return [Vertex(vertex, self.gameobj) for vertex in vertexList]
		
	def get_local_vector_to(self, position):
		return self.gameobj.getVectTo(position)[2]
		
	def set_color(self, color):
		self.gameobj.color = color
		
class Vertex:
	"""KX_VertexProxy wrapper"""
	def __init__(self, vertex, gameobj):
		ori = gameobj.worldOrientation
		self.x, self.y, self.z = (Matrix(ori[0], ori[1], ori[2])* Vector(vertex.getXYZ())) + Vector(gameobj.worldPosition)
class Engine:
	"""Wrapper for engine functionality"""
	
	def add_object(object, adder, time=0):
		"""Add an opject"""
		scene = gl.getCurrentScene()
		
		add = scene.addObject(object, adder.gameobj, time)
		return Object(add) if add else None
		
	def remove_object(object):
		"""Remove and object"""
		object.gameobj.endObject()
		
	def ray_cast(to_pos, from_pos, object, xray_prop=None):
		"""Cast a ray using the object"""
		
		ob, pos, norm = object.gameobj.rayCast(to_pos, from_pos, 0, xray_prop, 0, 1 if xray_prop else 0)
		
		return Object(ob) if ob else None, pos, norm
