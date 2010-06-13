# $Id$

# Description: Wraps a KX_GameObject to be used with the system
# Contributers: Mitchell Stokes

from mathutils import Matrix, Vector
import GameLogic as gl

# Movement modes
MOVE_LINV = 0
MOVE_FORCE = 1
MOVE_LOC = 2
MOVE_SERVO = 3
MOVE_POS = 4

class Object:
	"""KX_GameObject wrapper"""
	
	def __init__(self, gameobj, armature=None):
		self.gameobj = gameobj
		self.armature = armature
		# used for servo motion
		self.prev_error = Vector((0.0, 0.0, 0.0));
		self.tot_error = Vector((0.0, 0.0, 0.0));
		self.pid = [30.0, 0.5, 0.0]
		
	def move(self, vec, mode=MOVE_SERVO, min=[None, None, None], max=[None,None,None], local=True):
		"""Do object movement"""
		
		if mode == MOVE_LINV:
			self.gameobj.setLinearVelocity(vec, local)
		elif mode == MOVE_FORCE:
			self.gameobj.applyForce(vec, local)
		elif mode == MOVE_LOC:
			self.gameobj.applyMovement(vec, local)
		elif mode == MOVE_SERVO:
			target = Vector(vec)
			curr = self.gameobj.getLinearVelocity(local)
			error = target - curr
			self.tot_error += error
			dv = error - self.prev_error
			
			force = self.pid[0]*error + self.pid[1]*self.tot_error + self.pid[2]*dv
			
			# Handle limits
			for i in range(3):
				if min[i] != None and force[i] < min[i]:
					force[i] = min[i]
				if max[i] != None and force[i] > max[i]:
					force[i] = max[i]
			
			self.gameobj.applyForce(force, local)
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
		if not self.gameobj.invalid:
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
	
	def __init__(self, adder):
		self.adder = adder
	
	def add_object(self, object, pos=None, ori=None, time=0):
		"""Add an opject"""
		scene = gl.getCurrentScene()
		
		if pos: self.adder.worldPosition = pos
		if ori: self.adder.worldOrientation = ori
				
		add = scene.addObject(object, self.adder, time)
		return Object(add) if add else None
		
	def remove_object(self, object):
		"""Remove and object"""
		object.gameobj.endObject()
		
	def ray_cast(self, to_pos, from_pos, object, xray_prop=""):
		"""Cast a ray using the object"""
		
		ob, pos, norm = object.gameobj.rayCast(to_pos, from_pos, 0, xray_prop, 0, 1 if xray_prop else 0)
		
		return Object(ob) if ob else None, pos, norm
