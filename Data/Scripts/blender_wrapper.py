# $Id$

# Description: Wraps a KX_GameObject to be used with the system
# Contributers: Mitchell Stokes

from mathutils import Matrix, Vector
from cego import Node
from math import radians
import GameLogic as gl
import aud
import os

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
		
		# Set a property for accent color
		self.gameobj['accent'] = [0.5, 0.5, 0.5]
		
		# Create the socket dictionary
		if self._armature and self_armature.children:
			self.initialize_sockets()
		
		# used for servo motion
		self.prev_error = Vector((0.0, 0.0, 0.0));
		self.tot_error = Vector((0.0, 0.0, 0.0));
		self.pid = [30.0, 0.5, 0.0]
		
		# Stores the current animation
		self.animations = [""]*8
		
	def __eq__(self, other):
		self.gameobj == other.gameobj
	
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
		
	@property
	def scaling(self):
		return self.gameobj.localScale.copy()
		
	@scaling.setter
	def scaling(self, value):
		self.gameobj.localScale = value
		
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
	
	def play_action(self, actions, mode=0):		
		# Now play all of the actions in the set
		for i, v in enumerate(actions):
			if v['name'] != "*":
				self.play_animation(v['name'], v['start'], v['end'], mode=mode, layer=i)
			
		# Now clear the other layers
		for i in range(len(actions), len(self.animations)):
			self._armature.stopAction(i)
			self.animations[i] = ""
		
	def play_animation(self, anim, start=0, end=0, mode=0, layer=0, blending=0):
		if self._armature and anim != self.animations[layer]:
			self._armature.playAction(anim, start, end, play_mode=mode, layer=layer)
			self.animations[layer] = anim
			# self.gameobj.sendMessage("animation", anim, self._armature.name)
			
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
	
	def get_nav_nodes(self):
		nodes = []
		nav_mesh = None
		
		for child in self.gameobj.parent.children:
			if child.name.startswith("navmesh"):
				nav_mesh = child
				break
			
		if not nav_mesh:
			return nodes
		
		mesh = nav_mesh.meshes[0]
		
		for i in range(mesh.numPolygons):
			poly = mesh.getPolygon(i)
			verts = []
			for i in range(poly.getNumVertex()):
				verts.append(mesh.getVertex(poly.material_id, getattr(poly, "v"+str(i+1))))
				
			position = Vector((0,0,0))
			for i in range(poly.getNumVertex()):
				position = position + verts[i].XYZ
				
			position = position / poly.getNumVertex()
			position = nav_mesh.worldOrientation * position
			position = position + nav_mesh.worldPosition
			nodes.append(Node(position))
			
		return nodes
			
	def set_parent(self, parent):
		self.gameobj.setParent(parent.gameobj)
	
	@property
	def armature(self):
		return Object(self._armature)
		
	@armature.setter
	def armature(self, value):
		self._armature = value.gameobj
		# If the new object has children, try initializing sockets
		if self._armature.children:
			self.initialize_sockets()
		
	@property
	def color(self):
		return self.gameobj.color
	
	@color.setter
	def color(self, color):
		self.gameobj.color = color
		
		for c in self.gameobj.childrenRecursive:
			c.color = color
			
	@property
	def accent(self):
		return self.gameobj['accent']
	
	@accent.setter
	def accent(self, accent):
		self.gameobj['accent'] = accent
		
		for c in self.gameobj.childrenRecursive:
			c['accent'] = accent
		
	@property
	def visible(self):
		return self.gameobj.visible
		
	@visible.setter
	def visible(self, value):
		self.gameobj.visible = value
		
	@property
	def name(self):
		return self.gameobj.name
		
	@property
	def valid(self):
		return not self.gameobj.invalid
		
	@property
	def children(self):
		return [Object(child) for child in self.gameobj.children]
		
	def initialize_sockets(self):
		if not self._armature:
			print("WARNING: %s has no armature to contain sockets" % (self.gameobj.name))
			return
			
		if self._armature.children:
			self._sockets = {child.name.lower()[7:] : child for child in self._armature.children if child.name.lower().startswith("socket_")}
		else:
			print("WARNING: %s has no sockets" % self.gameobj.name)
		
	def socket_fill(self, socket_string, object):
		"""Fills the given socket with the given object"""
		if socket_string not in self._sockets:
			print("WARNING: No socket named %s" % socket_string)
			return
			
		socket = self._sockets[socket_string]
		object.position = socket.worldPosition
		object.set_orientation(socket.worldOrientation[:])
		object.gameobj.setParent(socket)
		
	def socket_clear(self, socket_string, object = None, delete=True):
		"""Clears the given item from the given socket. An object argument of None removes all items from the socket"""
		if socket_string not in self._sockets:
			print("WARNING: No socket named %s" % socket_string)
			return
			
		socket = self._sockets[socket_string]
		if object == None:
			for child in socket.children:
				child.removeParent()
				if delete:
					child.endObject()
			return
			
		if object.gameobj in socket.children:
			socket[object.gameobj].removeParent()
			if delete:
				socket[object.gameobj].endObject()
		else:
			print("WARNING: Object %s not in socket %s." % (object, socket_string))
		
		
class Vertex:
	"""KX_VertexProxy wrapper"""
	def __init__(self, vertex, gameobj):
		ori = gameobj.worldOrientation
		self.x, self.y, self.z = (Vector(vertex.getXYZ()) * Matrix(ori)) + Vector(gameobj.worldPosition)

class Camera:
	"""Wrapper for KX_Camera"""
	
	def __init__(self, pivot, target = None):
		# Set the pivot point, and try to find a camera
		self.pivot = pivot.gameobj
		for child in self.pivot.childrenRecursive:
			if child.name == "Camera":
				self.camera = child
				break
		else:
			print("WARNING: No camera found, assuming given pivot is camera")
			self.camera = self.pivot
			
		# Set up the target
		self.target = target
		
		# Make sure the camera has no local transformations
		self.camera.localPosition = (0, 0, 0)
		self.camera.localOrientation = (0, 0, 0)
		
		# A transition_point of 0 indicates no transitioning
		self._transition_point = 0
		self._transition_speed = 1
		
		self._old_position = 0
		self._old_orientation = 0
		self._old_distance = 0
		
		self.mode = ""
		self._mode_init = self.init_dummy
		self._mode_update = self.update_dummy
		
		self._target_position = 0
		self._target_orientation = 0
		self.camera.localPosition = (0, 0, 0)
		self._target_distance = 0
		
		self.camera.parent.timeOffset = 0
		
		self._first_frame = False
		
		# Whether or not to lock the camera
		self.lock = False
	
	def update(self, lock=False):
		self.lock = lock
		
		if self._transition_point != 0:
			# For the first frame save old data and run the mode's init function
			if self._first_frame:
				self._old_position = self.position.copy()
				self._old_orientation = self.pivot.localOrientation.copy()
				self._old_camera_pos = self.camera.localPosition.copy()
				# self._old_distance = self.camera.localPosition.copy()[2]
				self._mode_init()
				self._first_frame = False
				
			# Interpolate camera transition
			self.blend()

			# Increment the transition point
			self._transition_point += self._transition_speed
			# Flags the transition as finished
			if self._transition_point >= 1:
				self._transition_point = 0
		else:
			self._mode_update()
			
	def blend(self):
		x_diff = self._target_position - self._old_position
		ori_diff = self._target_orientation - self._old_orientation
		d_diff = self._target_distance - self._old_camera_pos[2]
		
		
		self.position += x_diff * self._transition_speed
		self.pivot.localOrientation = self._old_orientation + (ori_diff * self._transition_point)
		self.camera.localPosition += Vector((0, 0, d_diff)) * self._transition_speed
			
	def change_mode(self, mode_string="dummy", transition_time = 1):
		# Don't change modes if a change is already occuring
		if self._transition_point != 0:
			return
		
		# Don't change if already in the target mode
		if self.mode == mode_string:
			return
	
		# Make sure we don't get a number < 1
		if transition_time < 1:
			transition_time = 1
		# Check if the mode functions are defined
		if not hasattr(self, "init_" + mode_string) or not hasattr(self, "update_" + mode_string):
			print("WARNING: Mode %s not properly defined. Doing nothing." % (mode_string))
			return 
		
		self.mode = mode_string
		
		# Set mode functions
		self._mode_init = getattr(self, "init_" + mode_string)
		self._mode_update = getattr(self, "update_" + mode_string)
		
		# Set the transition point and speed
		self._transition_speed = 1/transition_time
		self._transition_point = 1/transition_time
		
		# Some defaults
		self.camera.perspective = 1
		self.camera.parent.timeOffset = 0
		self.camera.lens = 25
		self.camera.ortho_scale = 35
		
		self.pivot.setParent(self.target.gameobj)
		
		self.pivot.scaling = (1, 1, 1)
		
		self._first_frame = True
		
	def init_dummy(self):
		self._target_position = Vector((0, -2, 1.5))
		self._target_orientation = Matrix.Rotation(radians(90), 3, 'X')
		self._target_distance = 0
		return
		
	def update_dummy(self):
		return
		
	def init_shop(self):
		self._target_distance = 0
		self._target_position = Vector((1.75, 5, 2))		
		self._target_orientation = Matrix.Rotation(radians(100), 3, 'X') * Matrix.Rotation(radians(180), 3, 'Y')
		
		self.camera.lens = 40
		
	def update_shop(self):
		return
		
		
	def init_topdown(self):
		rotation = Matrix.Rotation(0, 3, 'X')
		
		self._target_orientation = rotation
		self._target_position = Vector((0, 0, 42))
		self._target_distance = 0
		
		self.camera.perspective = 0
		self.camera.parent.timeOffset = 25
		
	def update_topdown(self):
		# Avoid rotations
		if self.pivot.parent:
			self.pivot.removeParent()
			self.pivot.worldOrientation = self._target_orientation
		
		position = self.target.position + self._target_position
		self.pivot.worldPosition = position
		return
		
	def init_frankie(self):		
		self._target_distance = 2
		self._target_position = Vector((0, 0, 1.5))
		self._target_orientation = Matrix.Rotation(radians(80), 3, 'X')

		self.camera.parent.timeOffset = 35
		# self.camera.lens = 25
		return
		
	def update_frankie(self):
		# Move the camera in closer if something is in the way
		ray_hit = self.camera.rayCast(self.camera.worldPosition, self.pivot.worldPosition, self.camera.localPosition[2], "", 0, 0, 0,)[1]
		if ray_hit:
			scale = (ray_hit - self.pivot.worldPosition).length/self.camera.localPosition[2]
			if scale > 1:
				scale = 1
			elif scale < 0.1:
				scale = 0.1
		else:
			scale = 1
		
		if not self.lock:
			dy = 0.5 - gl.mouse.position[1]
			if abs(dy) > 0.01: # "Dead zone"
				x = self.pivot.localOrientation.to_euler("XYZ")[0]
	
				if radians(45) < x + dy < radians(115):
					self.pivot.applyRotation((dy, 0, 0), True)
			
			
		self.pivot.scaling = [scale, scale, scale]
		self.camera.scaling = [1/scale, 1/scale, 1/scale]
		
		return
		
	def init_combat(self):
		self.init_frankie()
		# self._target_orientation = Matrix.Rotation(radians(60), 3, 'X')
		
	def update_combat(self):
		self.update_frankie()
		
	def init_shoulder(self):
		self._target_distance = 0
		self._target_position = Vector((.5, -1.0, 1.5))
		self._target_rotation = Matrix.Rotation(radians(-90), 3, 'X')
		
	def update_shoulder(self):
		return
		
		
		
	def init_isometric(self):
		rotation = Matrix.Rotation(radians(45), 3, 'Z') * Matrix.Rotation(radians(35.246), 3, 'X') 
		
		self._target_orientation = rotation
		self._target_position = Vector((7, -7, 15))
		self._target_distance = 0
		
		self.camera.perspective = 0
		return
		
	def update_isometric(self):
		# Avoid rotations
		if self.pivot.parent:
			self.pivot.removeParent()
			self.pivot.worldOrientation = self._target_orientation
		
		position = self.target.position + self._target_position
		self.pivot.worldPosition = position
		return
		
	@property
	def target(self):
		return self._target
	
	@target.setter
	def target(self, value):
		self._target = value
		self.pivot.setParent(value.gameobj)
		
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
		
	@property
	def position(self):
		return self.pivot.localPosition.copy()
	@position.setter
	def position(self, value):
		self.pivot.localPosition = value

class Engine:
	"""Wrapper for engine functionality"""
	
	audio_folder = "Audio"
	
	def __init__(self, adder):
		self.adder = adder
		
		# So we can keep track of already loaded libraries
		self.library_list = []
		
		# Handle for background music
		self.bgm_handle = None
		self.bgm_file = None
		
		# XXX This should be replaced by some user setting
		self.volume = 0.0
		
		# Setup some default options
		self.options = {
					'x_sensitivity': 1.5,
					'y_sensitivity': 1.5,
				}
	
	def load_library(self, package, type='Scene'):
		"""Load scene data from a package file"""
		pname = package.__class__.__name__+":"+package.name
		# Don't load libraries multiple times
		if pname in self.library_list:
			return
			
		gl.LibLoad(pname, type, package.blend, load_actions=True)
		self.library_list.append(pname)
		
	def free_libraries(self):
		"""Free all the cached libraries"""
		
		for lib in self.library_list:
			print("Freeing:", lib)
			gl.LibFree(lib)
			
		self.library_list = []
		
	def angle_between(self, vec1, vec2):
		vec1 = Vector(vec1)
		vec2 = Vector(vec2)
		
		return vec1.angle(vec2)
	
	def add_object(self, object, pos=None, ori=None, time=0):
		"""Add an object"""
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
		if type(camera) == str:
			scene = gl.getCurrentScene()
			camera = scene.cameras[camera]
			scene.active_camera = camera
		else:
			gl.getCurrentScene().active_camera = camera.camera
		
	def ray_cast(self, to_pos, from_pos, object, xray_prop=""):
		"""Cast a ray using the object"""
		
		ob, pos, norm = object.gameobj.rayCast(to_pos, from_pos, 0, xray_prop, 0, 1 if xray_prop else 0)
		
		return Object(ob), pos, norm if ob else None, pos, norm
		
	@property
	def fps(self):
		"""The current fps"""
		return gl.getAverageFrameRate()

	#===========================================================================
	# Audio API
	#===========================================================================
	
	@property
	def volume(self):
		"""The audio volume"""
		return aud.device().volume
	
	@volume.setter
	def volume(self, value):
		aud.device().volume = value
	
	def play_bgm(self, music):
		if self.bgm_handle:
			# Fade out the previous music
			p = self.bgm_handle.position
			self.bgm_handle.stop()
			
			f = aud.Factory(self.bgm_file).fadeout(p, 1)
			aud.device().play(f).position = p
			
		# Now fadein the new music
		af = os.path.join(self.audio_folder, music)
		self.bgm_handle = aud.device().play(aud.Factory(af).fadein(0, 2))
		self.bgm_handle.loop_count = -1
		self.bgm_file = af
		
	def stop_bgm(self):
		if self.bgm_handle:
			self.bgm_handle.stop()
			self.bgm_handle = None
			self.bgm_file = None
	