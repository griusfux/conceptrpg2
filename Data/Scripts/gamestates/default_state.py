# $Id$

from Scripts.packages import *
from Scripts.mathutils import Vector
from Scripts.character_logic import PlayerLogic, MonsterLogic
from .base_state import *

class DefaultState(BaseState, BaseController):
	"""The default state for the game"""
			
	##########
	# Client
	##########
	
	client_functions = BaseState.client_functions.copy()
	server_functions = BaseState.server_functions.copy()
				
	# Client functions
	@rpc(client_functions, "position", str, float, float, float)
	def position(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		if main['player'].id == cid:
			# Check to make sure we are still where the server says we are
			server_pos = [x, y, z]
			client_pos = main['net_players'][cid].object.position
			
			for i in range(3):
				if abs(server_pos[i]-client_pos[i]) > 1.0:
					client_pos[i] = server_pos[i]
			main['net_players'][cid].object.position = client_pos
		else:
			main['net_players'][cid].object.position = (x, y, z)
		
	@rpc(client_functions, "move", str, float, float, float)
	def move(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		main['net_players'][cid].object.move([x, y, z], min=[-50, -50, 0], max=[50, 50, 0])
		
	@rpc(client_functions, "rotate", str, float, float, float)
	def rotate(self, main, cid, x, y, z):
		if cid not in main['net_players']: return
		main['net_players'][cid].object.rotate((x, y, z))
		
	@rpc(client_functions, "anim", str, str, int, int, int, int)	
	def anim(self, main, cid, action, start, end, layer, blending):
		if cid not in main['net_players']: return
		print("Playing", action)
		main['net_players'][cid].object.play_animation(action, start, end, layer, blending)
		
	@rpc(client_functions, "init_combat", str, int)
	def init_combat(self, main, room_id, owns):
		main['room'] = main['dgen'].rooms[room_id]
		
		main['combat_id'] = room_id
		main['owns_combat'] = owns != 0
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("default_state")
		main['engine'].set_active_camera(main['camera'])
		self.camera_mode = "frankie"
		
		main['full_map'] = False
		
		main['player'].save()
		
		self.in_shop = False
		
	def client_run(self, main):
		"""Client-side run method"""
		main['effect_system'].update()
		
		# Make sure the camera is in the right mode
		if main['camera'].mode != self.camera_mode:
			main['camera'].change_mode(self.camera_mode, 30)
		main['camera'].update()
		main['full_map'] = False
		
		# While the camera is still transitioning, do nothing
		if main['camera']._transition_point != 0:
			return

		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Handle item pickup
		self._handle_item_pickup(main)

		# Our id so we can talk with the server
		id = main['client'].id
		
		if inputs:
			if ("SwitchCamera", "INPUT_ACTIVE") in inputs:
				main['full_map'] = True

			if ("Character", "INPUT_CLICK") in inputs:
				main['overlay'] = "PlayerStats"
				return("Player", "PUSH")

			if ("Powers", "INPUT_CLICK") in inputs:
				main['overlay'] = "Powers"
				return("Player", "PUSH")

			if ("Inventory", "INPUT_CLICK") in inputs:
				main['overlay'] = "Inventory"
				return("Player", "PUSH")
				
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
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		del main['full_map']
			
	def _get_idle_animation(self, main):
		return main['default_actions']['default_idle']
		
	def _get_forward_animation(self, main):
		return main['default_actions']['default_walk']
	
	def _handle_item_pickup(self, main):
		for id in main['item_collisions']:
			if id in main['ground_items']:
				self.server.invoke("request_item_pickup", id)
			main['item_collisions'].remove(id)
			
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
				self.play_animation(main['player'], act, mode=1)
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
			self.play_animation(main['player'], act, mode=1)

		# Send the message
		# self.server.invoke("move", id, *movement)
		main['player'].object.move(movement, min=[-50, -50, 0], max=[50, 50, 0])

	##########
	# Server
	##########
		
	# Server functions
	@rpc(server_functions, "position", str, float, float, float)
	def position(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		if cid not in main['players']: return
		
		self.clients.invoke('position', cid, x, y, z)
		main['players'][cid].position = (x, y, z)
		
	@rpc(server_functions, "move", str, float, float, float)
	def move(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		# print(cid)
		self.clients.invoke('move', cid, x, y, z)
		
	@rpc(server_functions, "rotate", str, float, float, float)
	def rotate(self, main, client, cid, x, y, z):
		# We could run checks here, but for now we just rebroadcast
		self.clients.invoke('rotate', cid, x, y, z)
		
	@rpc(server_functions, "anim", str, int, int, int, int)
	def anim(self, main, client, action, start, end, layer, blending):
		self.clients.invoke("anim", client.id, action, start, end, layer, blending)

	@rpc(server_functions, "request_item_pickup", int)
	def request_item_pickup(self, main, client, id):
		# If the item is available, give it to the player
		if id in main['ground_items']:
			self.client.invoke("pickup_item", main['ground_items'][id])
			
		# Now remove the item from the ground for everyone
		self.clients.invoke("remove_item", id)

	@rpc(server_functions, "init_combat", str)
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
	
	# Empty ---
