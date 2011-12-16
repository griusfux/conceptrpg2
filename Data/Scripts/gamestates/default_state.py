# $Id$

import time

from Scripts.packages import *
from Scripts.mathutils import Vector
from Scripts.character_logic import PlayerLogic, MonsterLogic
from Scripts import effects
from .base_state import *

# A constant for how many frames are in a "turn"
TURN = 120

class DefaultState(BaseState, BaseController):
	"""The default state for the game"""
			
	client_functions = BaseState.client_functions.copy()
	server_functions = BaseState.server_functions.copy()
	
	ui_layout = "default_state"
	
	##########
	# Client
	##########
				
	# Client functions
	@rpc(client_functions, "position", str, float, float, float)
	def position(self, main, cid, x, y, z):
		if cid not in main['net_players']: return

		# Check to make sure we are still where the server says we are
		server_pos = [x, y, z]
		client_pos = main['net_players'][cid].position
		
		for i in range(3):
			if abs(server_pos[i]-client_pos[i]) > 0.5:
				client_pos[i] = server_pos[i]
		main['net_players'][cid].position = client_pos
		
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
	
	@rpc(client_functions, "add_status", str, str)	
	def c_add_status(self, main, cid, status):
		if cid not in main['net_players']: return
		
		try:
			status = Status(status)
		except (PackageError):
			print("WARNING: The status \"%s\" was not found" % status)
			return
		
		status.push(self, main['net_players'][cid])
		main['net_players'][cid].statuses.append(status)
		
	@rpc(client_functions, "remove_status", str, str)
	def c_remove_status(self, main, cid, status):
		if cid not in main['net_players']: return
		
		player = main['net_players'][cid]
		for i in player.statuses[:]:
			if i.name == status:
				player.statuses.remove(i)
				i.pop(self, player)
		

	@rpc(client_functions, "modify_health", str, float)
	def c_modify_health(self, main, cid, amount):
		if cid not in main['net_players']: return
		
		player = main['net_players'][cid]
		
		player.hp += amount
		if player.hp < 0: player.hp = 0
		
	@rpc(client_functions, "kill_player", str)
	def kill_player(self, main, cid):
		if cid != main['player'].id: return
		
		self._next_state = "Dead"
		
	@rpc(client_functions, "init_combat", str, int)
	def init_combat(self, main, room_id, owns):
		main['room'] = main['dgen'].rooms[room_id]
		
		main['combat_id'] = room_id
		main['owns_combat'] = owns != 0
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['engine'].set_active_camera(main['camera'])
		main['engine'].play_bgm('The Cannery.mp3')
		self.camera_mode = "frankie"
		
		main['full_map'] = False
		
		player = main['player']
		
		player.save()

		# Center the mouse so the character isn't staring up or down when the game starts
		main['input_system'].mouse.position = (0.5, 0.5)
		
		self.in_shop = False
		
		self.item_effects = []
		
		# Make sure the player is holding their weapon if they have one
		player.reset_weapon_mesh(main['engine'])
		
		# Some helpful tutorials for the player
		self.display_tutorial(player, "Controls")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		main['effect_system'].update()
		
		# Make sure the camera is in the right mode
		if not self.suspended:
			if main['camera'].mode != self.camera_mode:
				main['camera'].change_mode(self.camera_mode, 30)
			main['camera'].update(lock=main['player'].lock)
			main['full_map'] = False
			
			# While the camera is still transitioning, do nothing
			if main['camera']._transition_point != 0:
				return

		# Display any queued tutorials
		if main['tutorial_queue']:
			# Peek at the first item
			tutorial = main['tutorial_queue'].pop()
		
			# Note that the player has seen the tutorial\
			main['player'].tutorials.append(tutorial)

			# Display the tutorial			
			main['tutorial_string'] = tutorial
			return("Tutorial", "PUSH")
			
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()

		# Our id so we can talk with the server
		id = main['client'].id
		
		if inputs and not self.suspended:
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
		room_id = main['dgen'].get_id_from_message(main['encounter_message'])
		if room_id:
			self.server.invoke('init_combat', room_id)

		if main['room']:
			return ('Combat', 'SWITCH')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		del main['full_map']
		for i in self.item_effects:
			main['effect_systm'].remove(i)

	def _handle_generic_input(self, main, inputs):
		# Our id so we can talk with the server
		id = main['client'].id
		
		player = main['player']
		
		# Our movement vector and player speed
		movement = [0.0, 0.0, 0.0]
		speed = player.speed
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
			
		if ("Stats", "INPUT_CLICK") in inputs:
			main['ui_system'].toogle_overlay("stats")
			
		if ("Action", "INPUT_CLICK") in inputs:
			for k, v in main['ground_items'].items():
				if (Vector(v[1].position) - player.position).length < 1:
					self.server.invoke("request_item_pickup", k)
		if ("ShowItemNames", "INPUT_ACTIVE") in inputs:
			for k, v in main['ground_items'].items():
				if v[2] is None:
					pos = v[1].position[:2] + (v[1].position[2]+0.5,)
					effect = effects.TextEffect(v[0].name, pos, duration=1000,
												continuous=0, static=True)
					v[2] = main['effect_system'].add(effect)
		elif ("ShowItemNames", "INPUT_RELEASE") in inputs:
			for k, v in main['ground_items'].items():
				if v[2] is not None:
					main['effect_system'].remove(v[2])
					v[2] = None

		# Only let the player do stuff while they are not "locked"
		if not player.lock:
			# Update rotations (mouse look)
			dx = 0.5 - main['input_system'].mouse.position[0]
			if not player.auto_target and abs(dx) > 0:
				self.server.invoke("rotate", id, 0, 0, dx*main['engine'].options['x_sensitivity'])
			main['input_system'].mouse.position = (0.5, 0.5)

			if 'HELD' not in player.flags:
				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					movement[1] = speed
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					movement[1] = -speed
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					movement[0] = speed
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					movement[0] = -speed
				
		
		# Normalize the vector to the character's speed
		if movement != [0.0, 0.0, 0.0]:
			player.auto_target = player.auto_power = None
			movement = [float(i) for i in (Vector(movement).normalized()*speed)]
			self.server.invoke("position", id, *player.position)
			act = player.get_action("Move")
			self.play_animation(player, act, mode=1)
		elif player.auto_target:
			if "WEAPON_RANGE" in player.auto_power.flags:
				range = player.weapon.range
			else:
				range = player.auto_power.distance
				
			range += player.auto_target.size
			# vec = self.auto_target.object.position - player.object.position
			# distance = vec.dot(vec)
			# We shouldn't be calling getVectTo() like this, but it works and I can't get my copy to work.
			# I've left my code in here in case I want to try again.
			distance, unused, vec = player.object.gameobj.getVectTo(player.auto_target.object.gameobj)
			ang = Vector(vec[:2]).angle(Vector([0, 1]), 0)

			if distance < range and ang < 0.2:#*range:
				player.auto_power.use(self, player)
				player.auto_power.timer = player.auto_power.cool_down * TURN
				player.auto_power = player.auto_target = None
			else:
				# vec.normalize()
				# vec = player.object.get_orientation() * vec

				movement = [float(i) for i in vec*speed]
				movement[2] = 0
				self.server.invoke("position", id, *player.position)

				rot = 0
				if ang > 0.2:
					rot = 0.1
				if vec[0] > 0:
					rot = -rot

				self.server.invoke("rotate", id, 0, 0, rot)
				
				act = player.get_action("Move")
				self.play_animation(player, act, mode=1)

		# Otherwise, idle
		elif not player.lock:
			act = player.get_action("Idle")
			self.play_animation(player, act, mode=1)

		# Send the message
		# self.server.invoke("move", id, *movement)
		player.object.move(movement, min=[-50, -50, 0], max=[50, 50, 0])

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
		
	@rpc(server_functions, "add_status", str, str, float, int)
	def s_add_status(self, main, client, cid, status, amount, duration):
		try:
			_status = Status(status)
		except (PackageError):
			print("WARNING: The status \"%s\" was not found" % status)
			return
		_status.amount = amount
		_status.time = duration
		
		character = main['players'][cid]
		_status.push(self, character)
		character.statuses.append(_status)
		
		self.clients.invoke("add_status", cid, status)

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
		self.time = time.time()
		self.accum = 0
		
	def server_run(self, main, client):
		"""Server-side run method"""
		# This function is locked to 60/TURN executions per second
		new_time = time.time()
		self.accum += new_time - self.time
		self.time = new_time
		
		dt = 1/60 * TURN # Convert turns to seconds
		while self.accum >= dt:
			for player in main['players'].values():
				for status in player.statuses:
					status.use(self, player)
					status.time -= 1
					
					if status.time <= 0:
						status.pop(self, player)
						player.statuses.remove(status)
						self.clients.invoke("remove_status", player.id, status.name)
			self.accum -= dt

	##########
	# Other
	##########
	
	# Empty ---
	
	##########
	# Controller
	##########
		
	def add_status(self, character, status, amount, duration):		
		self.server.invoke("add_status", character.id, status, amount, duration)
	
	def animate_lock(self, character, animation):
		"""Convenience function that automatically sets the lock and mode for an animation
		
		character -- the character attacking
		animation -- the attack animation to use
		
		"""
				
		if not character.action_set:
			print("WARNING: attempting to animate character with an empty action set: %s. Skipping..." % character)
			return
		
		if animation not in self.main['actions'][character.action_set]:
			print("WARNING: animation \"%s\" not found in the action set \"%s\"" % (animation, character.action_set))
			character.add_lock(30)
			return
		
		actions = self.main['actions'][character.action_set][animation]
		lock = 0
		for layer in actions:
			duration = layer['end'] - layer['start']
			if duration > lock:
				lock = duration
				
		self.play_animation(character, animation, lock=lock, mode=0)
		
	def animate_weapon(self, character, animation):
		"""This function is used for when an attack animation is played"""
		self.animate_lock(character, animation)
		
	def animate_spell(self, character, animation):
		"""This function exists in case we want to handle spells and attacks differently, e.g. speed"""
		self.animate_lock(character, animation)
