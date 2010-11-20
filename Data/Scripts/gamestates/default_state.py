# $Id$

from Scripts.mathutils import Vector
from Scripts.character_logic import PlayerLogic
from .base_state import BaseState, BaseController

class DefaultState(BaseState, BaseController):
	"""The default state for the game"""
	
	def __init__(self, main, is_server=False):
		"""DefaultState Constructor"""
		
		BaseState.__init__(self, main, is_server)
			
	##########
	# Client
	##########
				
	# Client functions
	def position(self, main, cid, x, y, z):
		server_pos = [x, y, z]
		client_pos = main['net_players'][cid].object.position
		
		for i in range(3):
			if abs(server_pos[i]-client_pos[i]) > 1.0:
				client_pos[i] = server_pos[i]
			
		main['net_players'][cid].object.position = client_pos
		
	def move(self, main, cid, x, y, z):
		main['net_players'][cid].object.move([x, y, z], min=[-50, -50, 0], max=[50, 50, 0])
		
	def rotate(self, main, cid, x, y, z):
		main['net_players'][cid].object.rotate((x, y, z))
			
	def anim(self, main, cid, action, start, end, layer, blending):
		print("Playing", action)
		main['net_players'][cid].object.play_animation(action, start, end, layer, blending)
		
	# Override BaseState's to
	def to(self, main, id):
		if id not in main['net_players']: return
		
		main['net_players'][cid].end()
		del main['net_players'][cid]
		print(cid, "timed out.")
		
	# Override BaseState's dis
	def dis(self, main, id):
		if id not in main['net_players']: return
		
		main['net_players'][cid].end()
		del main['net_players'][cid]
		print(cid, "diconnected.")
	
	# Register the functions
	client_functions = {
				position: (str, float, float, float),
				move: (str, float, float, float),
				rotate: (str, float, float, float),
				anim: (str, str, int, int, int, int)
			}
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("default_state")
		main['camera'].change_mode("frankie")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# Reset the camera
		# old_ori = main['3p_cam'].world_orientation
		# main['3p_cam'].reset_orientation()
		# main['player'].object.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['camera'])
		main['camera'].update()
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()

		# Our id so we can talk with the server
		id = main['client'].id
			
		# Update our position
		# pos = main['player'].object.position
		# self.server.invoke('position', id, *pos)
		
		# Our movement vector and player speed
		movement = [0.0, 0.0, 0.0]
		speed = main['player'].speed
		
		if inputs:
			if ("SwitchCamera", "INPUT_CLICK") in inputs:
				# main['engine'].set_active_camera(main['top_down_camera'])
				if main['camera'].mode == "frankie":
					main['camera'].change_mode("topdown", 90)
				else:
					main['camera'].change_mode("frankie", 90)
				
			if ("Stats", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("stats")				
				
			if ("Inventory", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("inventory_overlay")
		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				# Update rotations (mouse look)
				dx = 0.5 - main['input_system'].mouse.position[0]
				if abs(dx) > 0:
					self.server.invoke("rotate", id, 0, 0, dx)
				main['input_system'].mouse.position = (0.5, 0.5)
				
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].powers.active.use(self, main['player'])
				if ("NextPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_next_active()
				if ("PrevPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_prev_active()

				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					movement[1] = speed
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					movement[1] = -speed
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					movement[0] = speed
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					movement[0] = -speed
				if ("MoveForward", "MoveBackward", "MoveRight", "MoveLeft", "INPUT_ACTIVE") not in inputs:
					act = main['default_actions']['default_idle']
					main['player'].object.play_animation(act['name'], act['start'], act['end'])
	
		# Normalize the vector to the character's speed
		if movement != [0.0, 0.0, 0.0]:
			movement = [float(i) for i in (Vector(movement).normalize()*speed)]

		# Send the message
		self.server.invoke("move", id, *movement)
		
		# Check to see if we need to move to the combat state
		# XXX This needs cleanup, we shouldn't be accessing KX_GameObject attributes
		if main.sensors['encounter_mess'].positive:
			import Scripts.blender_wrapper as Blender
			room = main['dgen'].rooms[main.sensors['encounter_mess'].bodies[0]]
			del room['encounter']
			main['room'] = Blender.Object(room)
			main['client'].send('stateCombat')
			return ('Combat', 'SWITCH')
			
	##########
	# Server
	##########
		
	# Server functions
	def position(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('position', cid, x, y, z)
		
	def move(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('move', cid, x, y, z)
		
	def rotate(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('rotate', cid, x, y, z)
		
	def anim(self, main, client, action, start, end, layer, blending):
		self.clients.invoke("anim", client.id, action, start, end, layer, blending)

	# Register the functions
	server_functions = {
				position: (str, float, float, float),
				move: (str, float, float, float),
				rotate: (str, float, float, float),
				anim: (str, int, int, int, int)
			}
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""
		pass
		
	##########
	# Other
	##########
	
	# Empty ---
	
	##########
	# Controller
	##########
	
	def play_animation(self, character, animation, lock=0):
		"""Instruct the character to play the animation
		
		character -- the character who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		character.add_lock(lock)
		self.server.invoke("anim", animation, 1, 20, 0, 0)
#		self.main['client'].send('anim:'+animation) # XXX should be done based on the supplied character
		
	def get_targets(self, type, range):
		"""Get targets in a range
		
		type -- the type of area (line, burst, etc)
		range -- the range to grab (integer)
		
		"""
		
		return []
