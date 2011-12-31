# $Id$

import time
import random
import math

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
		
		nplayer = main['net_players'][cid]

		# Check to make sure we are still where the server says we are
		server_pos = [x, y, z]
		client_pos = nplayer.position
		
		if cid == main['player'].id or (isinstance(nplayer, MonsterLogic) and main['is_host']):
			for i in range(3):
				if abs(server_pos[i]-client_pos[i]) > 0.5:
					client_pos[i] = server_pos[i]
				
			nplayer.position = client_pos
		else:
			nplayer.ipo_target = Vector(server_pos)
		
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
		main['net_players'][cid].object.play_animation(action, start, end, layer, blending)
	
	@rpc(client_functions, "add_status", str, str, float)	
	def c_add_status(self, main, cid, status, amount):
		if cid not in main['net_players']: return
		
		try:
			status = Status(status)
		except (PackageError):
			print("WARNING: The status \"%s\" was not found" % status)
			return
		
		status.amount = amount
		main['net_players'][cid].add_status(self, status)
		
	@rpc(client_functions, "remove_status", str, str)
	def c_remove_status(self, main, cid, status):
		if cid not in main['net_players']: return
		
		player = main['net_players'][cid]
		player.remove_status(self, status)

	@rpc(client_functions, "modify_health", str, float)
	def c_modify_health(self, main, cid, amount):
		if cid not in main['net_players']: return
		
		player = main['net_players'][cid]
		
		player.hp += amount
		if player.hp < 0: player.hp = 0
		
	@rpc(client_functions, "add_effect", "pickle", str, int)
	def c_add_effect(self, main, info, cid, id):
		if cid == main['player'].id: return
		
		effect = getattr(effects, info['type'])
		effect = effect.create_from_info(info, main['net_players'])
		main['effect_system'].add_remote(effect, id)
		
	@rpc(client_functions, "update_effect_remote_id", int, int)
	def c_update_effect_rid(self, main, lid, rid):
		main['effect_system'].update_remote_id(lid, rid)
		
	@rpc(client_functions, "end_effect", str, int)
	def c_end_effect(self, main, cid, remote_id):
		if cid == main['player'].id: return
		main['effect_system'].remove_remote(remote_id)
		
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
		
		main['player'].powers.update_cooldown()
		
		# Handles input
		inputs = main['input_system'].run()

		# Our id so we can talk with the server
		id = main['client'].id
		
		if not self.suspended:
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
			
	def _display_item_name(self, main, itemv):
		if itemv[2] is None:
			pos = itemv[1].position[:2] + (itemv[1].position[2]+0.5,)
			effect = effects.TextEffect(itemv[0].name, pos, duration=1000,
										continuous=0, static=True)
			itemv[2] = main['effect_system'].add(effect)
			
	def _remove_item_name(self, main, itemv):
		if itemv[2] is not None:
			main['effect_system'].remove(itemv[2])
			itemv[2] = None

	def _handle_generic_input(self, main, inputs):
		# Our id so we can talk with the server
		id = main['client'].id
		
		player = main['player']
		
		# Our movement vector and player speed
		movement = [0.0, 0.0, 0.0]
		speed = player.speed
		
		# This propagates player.recalc_stat over the network
		if player.network_update:
			self.server.invoke("update_player_info", player.get_info())
			player.network_update = False
		
		# Find the items in range here so we don't have to calculate twice
		# (once to display names and again for picking up items)
		items_to_display = items_in_range = {k: v for k, v in main['ground_items'].items() if (Vector(v[1].position).xy-player.position.xy).length_squared < 2}
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return("InGameMenu", "PUSH")
			
		if ("Stats", "INPUT_CLICK") in inputs:
			main['ui_system'].toogle_overlay("stats")
			
		if ("Action", "INPUT_CLICK") in inputs:
			for key in items_in_range:
				self.server.invoke("request_item_pickup", key)
		if ("ShowItemNames", "INPUT_ACTIVE") in inputs:
			items_to_display = main['ground_items']

		if not player.lock:
			if ("UsePower", "INPUT_CLICK") in inputs:
				self.use_power(player, player.powers.active)
			if ("UsePowerOne", "INPUT_CLICK") in inputs:
				if player.powers.has_power(0):
					self.use_power(player, player.powers.all[0])
			if ("UsePowerTwo", "INPUT_CLICK") in inputs:
				if player.powers.has_power(1):
					self.use_power(player, player.powers.all[1])
			if ("UsePowerThree", "INPUT_CLICK") in inputs:
				if player.powers.has_power(2):
					self.use_power(player, player.powers.all[2])
			if ("UsePowerFour", "INPUT_CLICK") in inputs:
				if player.powers.has_power(3):
					self.use_power(player, player.powers.all[3])
			if ("UsePowerFive", "INPUT_CLICK") in inputs:
				if player.powers.has_power(4):
					self.use_power(player, player.powers.all[4])
			if ("UsePowerSix", "INPUT_CLICK") in inputs:
				if player.powers.has_power(5):
					self.use_power(player, player.powers.all[5])

		if ("NextPower", "INPUT_CLICK") in inputs:
			player.powers.make_next_active()
		if ("PrevPower", "INPUT_CLICK") in inputs:
			player.powers.make_prev_active()
			
		# Now display all the names for items in range
		for k, v in main['ground_items'].items():
			if k in items_to_display:
				self._display_item_name(main, v)
			else:
				self._remove_item_name(main, v)

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
			
		# Interpolate netplayer positions
		for nplayer in [i for i in main['net_players'].values() if i !=player and i.ipo_target]:
			vec = nplayer.ipo_target - nplayer.position
			distance = vec.length_squared
	
			if distance > 100.0:
				nplayer.position = nplayer.ipo_target
			elif distance > 0.5:
				v = vec.normalized() * speed
				if v.length_squared > distance:
					nplayer.position = nplayer.ipo_target
				nplayer.position += v
			else:
				nplayer.position = nplayer.ipo_target

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
		character.add_status(self, _status)
		
		self.clients.invoke("add_status", cid, status, amount)
		
	@rpc(server_functions, "remove_status", str, str)
	def s_remove_status(self, main, client, cid, status):
		character = main['players'][cid]
		character.remove_status(self, status)
		self.clients.invoke("remove_status", cid, status)
		
	@rpc(server_functions, "add_effect", "pickle", int)
	def s_add_effect(self, main, client, info, local_id):
		main['effect_id'] += 1
		self.clients.invoke("add_effect", info, client.id, main['effect_id'])
		
		self.client.invoke("update_effect_remote_id", local_id, main['effect_id'])
		
	@rpc(server_functions, "end_effect", int)
	def s_end_effect(self, main, client, remote_id):
		self.clients.invoke("end_effect", client.id, remote_id)

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
	
	def remove_status(self, character, status):
		self.server.invoke("remove_status", character.id, status)
		
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
	
	# XXX Powers should no longer specify there casting animation!
	# We specify None here to keep powers from breaking until they are fixed.
	def animate_spell(self, character, animation=None):
		"""This function exists in case we want to handle spells and attacks differently, e.g. speed"""
		self.animate_lock(character, "Cast")

	def deal_damage(self, caster, target, power, damage, type, delay=0):
			damage += caster.affinities[power.element]
			damage -= target.affinities[power.element]
			
			type = type.upper()
			if type == "PHYSICAL":
				damage += caster.physical_damage
				damage -= target.physical_defense
			elif type == "ARCANE":
				damage += caster.arcane_damage
				damage -= target.arcane_defense
			else:
				print("WARNING: invalid type supplied to deal_damage() from power:", power.name)
			
			self.modify_health(target, -max(1, damage), delay=delay)
		
	def modify_health(self, character, amount, delay=0):
		BaseController.modify_health(self, character, amount)
		
		if not self.is_server:
			for i, v in self.monster_list.items():
				if character == v:
					self.server.invoke("modify_health", i, amount)
				
		text = amount if amount != 0 else "Missed"
		pos = list(character.position[:])
		pos[2] += 2
		effect = effects.TextEffect(text, pos, 90, delay=delay)
		self.add_effect(effect)
		
	def add_effect(self, effect):
		info = effect.get_info()
		
		if self.is_server:
			self.main['effect_id'] += 1
			self.clients.invoke("add_effect", info, "", self.main['effect_id'])
		else:
			self.main["effect_system"].add(effect)
			self.server.invoke("add_effect", info, effect.id)
			return effect.id
		
	def end_effect(self, id):
		effect_system = self.main["effect_system"]
		
		remote_id = effect_system.get_remote_id(id)
		effect_system.remove(id)

		if remote_id is not None:
			self.server.invoke("end_effect", remote_id)
		
	def get_potential_targets(self):
		l = []
		
		if self.is_server:
			combat = self.client_handle.server.main['combats'].get(self.client_handle.combat_id)
			if combat:
				l.extend(combat.hero_list.values())
				l.extend(combat.monster_list.values())
				
		return l
		
	def get_closest_target(self, character, targets):
		"""Get the closest target to the given character from the targets list"""
		
		cobj = character.object
		
		closest = None
		
		min_distance = 1000
		
		for target in targets:
			v = cobj.position - target.object.position
			distance2 = v.dot(v)

			if closest == None or distance2 < min_distance:
				closest = target
				min_distance = distance2
				
		return closest
	
	def get_next_target(self, current, targets):
		"""Get the next target in the targets list"""
		
		try:
			idx = targets.index(current)+1
		except ValueError:
			return None
		
		if idx >= len(targets):
			idx = 0
			
		return targets[idx]
		
	def get_prev_target(self, current, targets):
		"""Get the previous target in the targets list"""
		
		try:
			idx = targets.index(current) - 1
		except ValueError:
			return None
		
		# Negative numbers are fine, Python will just go to the back of the list, which we want.
		return targets[idx]
	
	def get_targets(self, power, character):
		if "WEAPON_RANGE" in power.flags:
			distance = character.weapon.range
		else:
			distance = power.distance
		
		return self.get_targets_ex(character, power.effect_shape, distance, power.target_mask)
		
	def get_targets_ex(self, character, shape, distance, target_types={'ENEMIES'}, source=None):
		"""Get targets in a range
		
		character -- character using the power
		shape -- the shape of area (line, burst, etc)
		range -- the range to grab (integer)
		target_types -- which type of targets to grab (SELF, ALLIES, ENEMIES, etc)
		
		"""

		# If we have a shape of "SELF" just return the character
		if shape == 'SELF':
			return [character]
		
		# Bump the range a bit to compensate for the first half "tile"
		# that the player occupies
		distance += character.size
		
		if not source:
			source = character.position

		targets = []
		
		if not target_types:
			return targets
			
		if self.is_server:
			combat = self.main['combats'].get(self.client_handle.combat_id, None)
			if not combat:
				hero_list = monster_list = {}
			else:
				hero_list = combat.hero_list
				monster_list = combat.monster_list
		else:
			hero_list = self.hero_list
			monster_list = self.monster_list

		tlist = []
		if 'SELF' in target_types:
			tlist.append(character)
		if 'ALLIES' in target_types:
			tlist.extend(hero_list.values() if character in hero_list.values() else monster_list.values())
		if 'ENEMIES' in target_types:
			tlist.extend(monster_list.values() if character in hero_list.values() else hero_list.values())
		
		if shape == 'ALL' or (self.is_server and shape == 'SINGLE'):
			targets = tlist
		elif shape == 'SINGLE':
			ori_ivnt = character.orientation.inverted()
			for target in tlist:
				# Convert to local space
				v = target.position - source
				v = ori_ivnt * v
				
				# Now do a simple bounds check
				if v[1] < distance + target.size and abs(v[0]) < target.size * 2: # Multiply by 2 to allow for more error
					targets.append(target)
		elif shape == 'BURST':
			for target in tlist:
				
				# Do a simple distance check
				if (target.position - source).length < distance:
					targets.append(target)
		elif shape == 'CONE':
			pi_fourths = math.pi / 4
			for target in tlist:
			
				# Start with a simple distance check
				if (target.position - source).length < distance:
					
					# Now do an angle check
					v1 = character.object.forward_vector
					v2 = target.position - character.position
					
					angle = v1.angle(v2, 0)
					
					if angle < pi_fourths:
						targets.append(target)

		return targets		
	
	def spawn(self, character, position):
		if hasattr(self, 'clients'):
			combat = self.main['combats'].get(self.client_handle.combat_id, None)
			if combat and character.id in combat.monster_list:
				self.animate_lock(character, "Spawn")
				combat.monster_list[character.id].position = position
				self.clients.invoke("position", character.id, *position)
	
	def move(self, character, linear = (0,0,0) , angular = (0,0,0) , local = False):
		"""Handles linear and angular movement of a character"""
		if "HELD" in character.flags:
			return
		if self.is_server:
			# The only people that should be moving server side are monsters
			self.clients.invoke("move_monster", character.id, *linear)
			self.clients.invoke("rotate_monster", character.id, *angular)
			self.play_animation(character, "Move", mode=1)
		else:
			# Move the character
			character.object.move(linear, min=[-50, -50, 0], max=[50, 50, 0], local=local)
			
			# Now handle rpcs
			self.server.invoke("rotate", character.id, *angular)
			self.server.invoke("position", character.id, *character.position)
		
	def reposition(self, character, position):
		character.object.position = position
		self.server.invoke("position", character.id, *character.object.position)
		
	def despawn(self, character):
		pass
	
	def attack(self, power, character, multiplier=1):
		# Fetching animation data to determine a delay
		action = character.get_action("Attack")
		animation = self.main['actions'][character.action_set][action]
		delay = (animation[0]['end'] - animation[0]['start'])
		
		self.animate_weapon(character, action)
		for target in self.get_targets(power, character):
			damage = character.weapon.damage*multiplier
			hit = character.accuracy + random.randint(1, 20) >= target.reflex + random.randint(1, 20)
			
			# Store state information for callbacks to modify
			state = {
						'HIT' : hit,
						'DAMAGE' : damage,
						'TARGET' : target,
						'TYPE' : 'PHYSICAL', 
					}
			
			# Address all the callbacks
			remove = []
			for name, callback in character.callbacks['ATTACK'].items():
				state, complete = callback(state)
				if complete:
					remove.append(name)
					
			# Clear out the complete callbacks		
			for name in remove: character.remove_callback(name, "ATTACK")
			
			if state['HIT']:
				if multiplier == 0: return
				
				self.deal_damage(character, state['TARGET'], power,
								state['DAMAGE'] , state['TYPE'], delay=delay/2)
			else:
				self.modify_health(target, 0, delay=delay)
	
	def use_power(self, character, power, auto_range=True):
		if isinstance(power, str):
			power = Power(power)
			
		if power.timer > 0:
			return
		if power.effect_shape == 'SELF' or not auto_range:
			power.use(self, character)
			power.timer = power.cool_down * TURN
		elif character.targets:
			character.auto_power = power
			character.auto_target = character.targets[0]
