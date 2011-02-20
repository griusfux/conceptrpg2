# $Id$

from Scripts.packages import *
from Scripts.mathutils import Vector
from Scripts.character_logic import PlayerLogic, MonsterLogic
from .base_state import BaseState, BaseController

class DefaultState(BaseState, BaseController):
	"""The default state for the game"""
			
	##########
	# Client
	##########
				
	# Client functions
	def position(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		server_pos = [x, y, z]
		client_pos = main['net_players'][cid].object.position
		
		for i in range(3):
			if abs(server_pos[i]-client_pos[i]) > 1.0:
				client_pos[i] = server_pos[i]
			
		main['net_players'][cid].object.position = client_pos
		
	def move(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		main['net_players'][cid].object.move([x, y, z], min=[-50, -50, 0], max=[50, 50, 0])
		
	def rotate(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		main['net_players'][cid].object.rotate((x, y, z))
			
	def anim(self, main, cid, action, start, end, layer, blending):
		if cid not in main['net_players']: return
		print("Playing", action)
		main['net_players'][cid].object.play_animation(action, start, end, layer, blending)
		
	def init_combat(self, main, room_id, owns):
		main['room'] = main['dgen'].rooms[room_id]
		
		main['combat_id'] = room_id
		main['owns_combat'] = owns != 0
		
		
	# Override BaseState's to
	def to(self, main, cid):
		if id not in main['net_players']: return
		
		main['net_players'][cid].object.end()
		del main['net_players'][cid]
		print(cid, "timed out.")
		
	# Override BaseState's dis
	def dis(self, main, cid):
		if id not in main['net_players']: return
		
		main['net_players'][cid].object.end()
		del main['net_players'][cid]
		print(cid, "diconnected.")
	
	# Register the functions
	client_functions = {
				"position": (position, (str, float, float, float)),
				"move": (move, (str, float, float, float)),
				"rotate": (rotate, (str, float, float, float)),
				"anim": (anim, (str, str, int, int, int, int)),
				"init_combat": (init_combat, (str, int)),
				"to": (to, (str,)),
				"dis": (dis, (str,)),
			}
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("default_state")
		main['engine'].set_active_camera(main['camera'])
		self.camera_mode = "frankie"
		
		main['player'].save()
		
		self.in_shop = False
		
	def client_run(self, main):
		"""Client-side run method"""
		main['effect_system'].update()
		
		# Make sure the camera is in the right mode
		if main['camera'].mode != self.camera_mode:
			main['camera'].change_mode(self.camera_mode, 60)
		main['camera'].update()
		
		# While the camera is still transitioning, do nothing
		if main['camera']._transition_point != 0:
			return

		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()

		# Our id so we can talk with the server
		id = main['client'].id
		
		if inputs:
			if ("SwitchCamera", "INPUT_CLICK") in inputs:
				# main['engine'].set_active_camera(main['top_down_camera'])
				if main['camera'].mode == "frankie":
					self.camera_mode = "topdown"
				else:
					self.camera_mode = "frankie"
				
			if main['player'].unspent_levels and ("LevelUp", "INPUT_CLICK") in inputs:
				return("LevelUp", "PUSH")

			if ("Inventory", "INPUT_CLICK") in inputs:
				main['ui_system'].toggle_overlay("inventory_overlay")
				
			if ("Action", "INPUT_CLICK") in inputs and not self.in_shop:
				for shop, obj in main['shop_keepers'].items():
					if (Vector(obj.position) - main['player'].object.position).length < 3:
						main['shop_keeper'] = shop
						main['shop_spot'] = obj
						return ("Shop", "PUSH")
				
			if ("Exp", "INPUT_CLICK") in inputs:
				main['player'].xp += 500
			
			# Camera switching
			if ("cam1", "INPUT_CLICK") in inputs:
					self.camera_mode = "frankie"
				
			if ("cam2", "INPUT_CLICK") in inputs:
					self.camera_mode = "topdown"
				
			if ("cam3", "INPUT_CLICK") in inputs:
					self.camera_mode = "isometric"
				
			if ("cam4", "INPUT_CLICK") in inputs:
					self.camera_mode = "dummy"
				
			if ("cam5", "INPUT_CLICK") in inputs:
					self.camera_mode = "shop"
			if ("cam6", "INPUT_CLICK") in inputs:
					self.camera_mode = "shoulder"
					
			
			result = self._handle_generic_input(main, inputs)
			if result:
				return result
		
		# Check to see if we need to move to the combat state
		# XXX This needs cleanup, we shouldn't be accessing KX_GameObject attributes
		if main.sensors['encounter_mess'].positive:
			import Scripts.blender_wrapper as Blender
			room_id = main.sensors['encounter_mess'].bodies[0]
			self.server.invoke("init_combat", room_id)
			room = main['dgen'].rooms[room_id]
			del room.gameobj['encounter']
			
			
		if main['room']:
			return ('Combat', 'SWITCH')
			
	def _get_idle_animation(self, main):
		return main['default_actions']['default_idle']
		
	def _get_forward_animation(self, main):
		return main['default_actions']['default_walk']
			
	def _handle_generic_input(self, main, inputs):
		# Our id so we can talk with the server
		id = main['client'].id
		
		# Our movement vector and player speed
		movement = [0.0, 0.0, 0.0]
		speed = main['player'].speed
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
			
		if ("Stats", "INPUT_CLICK") in inputs:
			main['ui_system'].toogle_overlay("stats")

		# Only let the player do stuff while they are not "locked"
		if not main['player'].lock:
			# Update rotations (mouse look)
			dx = 0.5 - main['input_system'].mouse.position[0]
			if abs(dx) > 0:
				self.server.invoke("rotate", id, 0, 0, dx)
			main['input_system'].mouse.position = (0.5, 0.5)

			if ("MoveForward", "INPUT_ACTIVE") in inputs:
				act = self._get_forward_animation(main)
				main['player'].object.play_animation(act['name'], act['start'], act['end'], mode=1)
				movement[1] = speed
			if ("MoveBackward", "INPUT_ACTIVE") in inputs:
				movement[1] = -speed
			if ("MoveRight", "INPUT_ACTIVE") in inputs:
				movement[0] = speed
			if ("MoveLeft", "INPUT_ACTIVE") in inputs:
				movement[0] = -speed
				
		
		# Normalize the vector to the character's speed
		if movement != [0.0, 0.0, 0.0]:
			movement = [float(i) for i in (Vector(movement).normalized()*speed)]
			self.server.invoke("position", id, *main['player'].object.position)

		# Otherwise, idle
		elif not main['player'].lock:
			act = self._get_idle_animation(main)
			main['player'].object.play_animation(act['name'], act['start'], act['end'], mode=1)

		# Send the message
		self.server.invoke("move", id, *movement)

	##########
	# Server
	##########
		
	# Server functions
	def position(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('position', cid, x, y, z)
		main['players'][cid].position = (x, y, z)
		
	def move(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		# print(cid)
		self.clients.invoke('move', cid, x, y, z)
		
	def rotate(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('rotate', cid, x, y, z)
		
	def anim(self, main, client, action, start, end, layer, blending):
		self.clients.invoke("anim", client.id, action, start, end, layer, blending)
		
	def init_combat(self, main, client, room_id):
		if main['encounters'].get(room_id):
			main['encounters'][room_id] = False
			main['combats'][room_id] = -1
			self._next_state = "Combat"
			client.combat_id = room_id
			self.client.invoke("init_combat", room_id, 1)
		elif main['combats'].get(room_id):
			self._next_state = "Combat"
			client.combat_id = room_id
			self.client.invoke("init_combat", room_id, 0)
			
	# Register the functions
	server_functions = {
				"position": (position, (str, float, float, float)),
				"move": (move, (str, float, float, float)),
				"rotate": (rotate, (str, float, float, float)),
				"anim": (anim, (str, int, int, int, int)),
				"init_combat": (init_combat, (str,))
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
