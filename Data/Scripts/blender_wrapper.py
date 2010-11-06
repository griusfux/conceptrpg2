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
		self._armature = armature
		# used for servo motion
		self.prev_error = Vector((0.0, 0.0, 0.0));
		self.tot_error = Vector((0.0, 0.0, 0.0));
		self.pid = [30.0, 0.5, 0.0]
		
	def __eq__(self, other):
		self.gameobj == other.gamobj
	
	def __ne__(self, other):
		self.gameobj != other.gameobj
		
	def __repr__(self):
		return self.gameobj.name
		
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
			
	def rotate(self, vec, local=True):
		"""Do object rotation"""
		
		self.gameobj.applyRotation(vec, local)
		
	@property
	def position(self):
		return self.gameobj.worldPosition.copy()
		
	@position.setter
	def position(self, value):
		self.gameobj.worldPosition = value[:]
		
	def get_orientation(self):
		return self.gameobj.worldOrientation
		
	def set_orientation(self, ori, local=False):
		vector = True
		try:
			len(ori[0])
			vector = False
		except TypeError:
			pass
		if vector:
			ori_vec = [float(i) for i in ori]
			y = Vector((ori_vec[0], ori_vec[1], ori_vec[2]))
			z = Vector((0.0, 0.0, 1.0))
			x = y.cross(z)
			ori = ([
						[x[0], y[0], z[0]],
						[x[1], y[1], z[1]],
						[x[2], y[2], z[2]]
						])
	
		if local:
			self.gameobj.localOrientation = ori[:]
		else:
			self.gameobj.worldOrientation = ori[:]
		
	@property
	def forward_vector(self):
		return self.gameobj.getAxisVect((0,1,0))
		
	def get_axis_vector(self, axis):
		sign = 1
		if len(axis) == 2:
			sign = -1
		else:
			axis = " " + axis
		
		ori = self.gameobj.localOrientation[:]
		vector = (0, 0, 0)
		if axis[1] == 'x':
			vector = (1, 0, 0)
		elif axis[1] == 'y':
			vector = (0, 1, 0)
		elif axis[1] == 'z':
			vector = (0, 0, 1)
		
		vector = [component*sign for component in vector]
		
		return vector
		
	def get_local_vector_to(self, position, arg = 2):
		return self.gameobj.getVectTo(position)[arg]	
		
	def play_animation(self, anim):
		if self._armature:
			self.gameobj.sendMessage("animation", anim, self._armature.name)
			
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
		
	def set_parent(self, parent):
		self.gameobj.setParent(parent.gameobj)
	
	@property
	def armature(self):
		return Object(self._armature)
		
	@armature.setter
	def armature(self, value):
		self._armature = value.gameobj
		
	@property
	def color(self):
		return self.gameobj.color
	
	@color.setter
	def color(self, color):
		self.gameobj.color = color
		
class Vertex:
	"""KX_VertexProxy wrapper"""
	def __init__(self, vertex, gameobj):
		ori = gameobj.worldOrientation
		self.x, self.y, self.z = (Matrix(ori[0], ori[1], ori[2])* Vector(vertex.getXYZ())) + Vector(gameobj.worldPosition)

class Camera:
	"""Wrapper for KX_Camera"""
	
	def __init__(self, camera, pivot=None):
		self.camera = camera
		self.pivot = pivot if pivot else camera
		
	@property
	def world_orientation(self):
		"""The camera's world orientation"""
		return [[x,y,z] for x, y, z in self.pivot.worldOrientation]

	@world_orientation.setter
	def world_orientation(self, value):
		self.pivot.worldOrientation = value
		
	@property
	def local_orientation(self):
		"""The camera's local orientation"""
		return [[x,y,z] for x, y, z in self.pivot.localOrientation]

	@local_orientation.setter
	def local_orientation(self, value):
		self.pivot.localOrientation = value

	def reset_orientation(self):
		self.pivot.localOrientation.identity()

class Engine:
	"""Wrapper for engine functionality"""
	
	def __init__(self, adder):
		self.adder = adder
		
		# So we can keep track of already loaded libraries
		self.library_list = []
	
	def load_library(self, package):
		"""Load scene data from a package file"""
		# Don't load libraries multiple times
		if package.name in self.library_list:
			return
			
		gl.LibLoad(package.name, 'Scene', package.blend)
		self.library_list.append(package.name)
		
	def angle_between(self, vec1, vec2):
		vec1 = Vector(vec1)
		vec2 = Vector(vec2)
		
		return vec1.angle(vec2)
	
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
		
	def add_network_player(self, ob_name):
		root = self.add_object("NetEmpty")
		player = self.add_object(ob_name)
		player.gameobj.setParent(root.gameobj)
		return player
		
	def set_active_camera(self, camera):
		"""Set the active camera"""
		
		gl.getCurrentScene().active_camera = camera.camera
		
	def ray_cast(self, to_pos, from_pos, object, xray_prop=""):
		"""Cast a ray using the object"""
		
		ob, pos, norm = object.gameobj.rayCast(to_pos, from_pos, 0, xray_prop, 0, 1 if xray_prop else 0)
		
		return Object(ob) if ob else None, pos, norm
		
	@property
	def fps(self):
		"""The current fps"""
		return gl.getAverageFrameRate()