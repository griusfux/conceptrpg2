# $Id$

from .base_state import *
from .default_state import DefaultState
from Scripts.packages import *
from Scripts.character_logic import MonsterLogic, PlayerLogic

import random
from math import *

import cego as AiManager
from cego.state_machine import StateMachine as AiStateMachine
from Scripts.mathutils import Vector, Matrix
import Scripts.effect_manager as effects
import Scripts.items as Items

# Constants for grid generation
UNIT_SIZE = 1
HALF_UNIT_SIZE = UNIT_SIZE/2.0
SAFE_Z = 0.01

class Combat:
	"""Combat utility class"""
	
	def __init__(self):
		self.hero_list = []
		self.monster_list = {}
		self.environment = []

class CombatState(DefaultState, BaseController):
	
	client_functions = DefaultState.client_functions.copy()
	server_functions = DefaultState.server_functions.copy()
	
	##########
	# Client
	##########
	
	@rpc(client_functions, "add_monster", str, str, str, float, float, float)
	def add_monster(self, main, cid, monster, id, x, y, z):
		if cid != main['combat_id']: return
		if id in self.monster_list: return
		
		if id not in main['net_players']:
			print("Warning, couldn't find MonsterLogic for id:", id)
			return
			
		# Add the monster to the monster list
		logic = main['net_players'][id]
		
		obj = logic.object
		self.monster_list[id] = logic
		
		color = obj.color
		color[3] = 0
		obj.color = color
	
		effect = effects.FadeEffect(obj, duration=90, amount=1)
		self.add_effect(effect)
		
	@rpc(client_functions, "kill_monster", str, str)
	def kill_monster(self, main, cid, id):
		if cid != main['combat_id']: return
		if id not in self.monster_list: return
		monster = self.monster_list[id]
		main['player'].xp += monster.xp_reward//len(self.hero_list)
		
		if monster in main['player'].targets:
			main['player'].targets.remove(monster)

		# Clear any of the monster's statuses out of the status list
		for status in self.status_list:
			if status['user'] == monster:
				self.status_list.remove(status)

		del self.monster_list[id]
		
	@rpc(client_functions, "move_monster", str, float, float, float)
	def move_monster(self, main, cid, x, y, z):
		if cid not in self.monster_list: return
		self.monster_list[cid].object.position = (x, y, z)
		
	@rpc(client_functions, "rotate_monster", str, float, float, float)
	def rotate_monster(self, main, cid, x, y, z):
		if cid not in self.monster_list: return
		self.monster_list[cid].object.rotate((x, y, z))

	@rpc(client_functions, "add_hero", str, str)
	def add_hero(self, main, cid, hid):
		if cid != main['combat_id']: return
		if hid in self.hero_list: return
		
		self.hero_list[hid] = main['net_players'][hid]
	
	@rpc(client_functions, "end_combat", str)
	def end_combat(self, main, cid):
		if cid != main['combat_id']: return
		self._next_state = "Default"
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		main['ui_system'].load_layout("combat")
		main['engine'].play_bgm('Take the Lead.mp3')
		
		self.monster_list = {}
		self.hero_list = {main['client'].id:main['player']}
		
		# Place the monsters
		if main['owns_combat']:
			nav_nodes =  main['room'].get_nav_nodes()
			for node in nav_nodes:
				self.server.invoke("add_node", node)
				
			self.server.invoke("set_environment")
			
			players = [i for i in main['net_players'].values() if isinstance(i, PlayerLogic)]
			num_players = len(players)
			
			party_level = 0
			for i in players:
				party_level += i.level
			party_level //= num_players
				
			for i, monster in enumerate(self._generate_encounter(main['dgen'].deck, num_players)):
				
				# Update the server
				self.server.invoke("add_monster", monster, party_level, str(i), 0, 0, SAFE_Z)
					
		else:
			# Request monsters from the server
			self.server.invoke("request_monsters")
			
			# Let others know we're here
			self.server.invoke("add_hero")
		
		# If the player has a weapon, socket it
		if main['player'].weapon:
			weapon = main['player'].weapon
			obj = weapon.createObjectInstance(main['engine'])
			main['player'].set_right_hand(obj)
			
		self.camera = 'combat'
		self.last_camera = 'frankie'
		
		self.status_list = []
			
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# Update the camera
		if self.camera != self.last_camera:
			main['camera'].change_mode(self.camera, 15)
			self.last_camera = self.camera
		else:
			main['camera'].update()
		self.camera = 'combat'
		
		# Update the effect system
		main['effect_system'].update()

		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Reset the target shapes
		for key, shape in main['target_shapes'].items():
			shape.visible = False
			
		# Handle status effects
		for status in self.status_list:
			status['time'] += 1
			if status['time'] == TURN:
				status['time'] = 0
				status['power'].use(self, status['user'])
				status['duration'] -= 1
				if status['duration'] <= 0:
					status['power'].pop(self, status['user'])
		
		# Targeting
		if not main['player'].targets:
			target = self.get_closest_target(main['player'], self.monster_list.values())
			if target:
				main['player'].targets = [target]
#		active_power = main['player'].powers.active
#		range_type = active_power.effect_shape
#		if "WEAPON_RANGE" in active_power.flags:
#			range_size = main['player'].weapon.range
#		else:
#			range_size = active_power.distance
#		if range_type == 'SINGLE':
#			# If the player already has targets, find out if they are valid
#			if main['player'].targets:
#				# Ranged can only have one target
#				if len(main['player'].targets) > 1:
#					main['player'].targets = []
#				else:
#					# The target must be in range
#					if (main['player'].targets[0].object.position-main['player'].object.position).length > range_size + HALF_UNIT_SIZE:
#						main['player'].targets = []
#			else:
#				target = None
#				target_dist = range_size + HALF_UNIT_SIZE
#				for monster in self.monster_list.values():
#					dist = (monster.object.position-main['player'].object.position).length
#					if dist < target_dist:
#						target = monster
#						target_dist = dist
#				main['player'].targets = [target,] if target else []
#		else:	
#			mask = getattr(active_power, "mask", {'ENEMIES'})
#			main['player'].targets = self.get_targets(main['player'], range_type, range_size, target_types=mask)		
		
		# Maintain monsters
		for id, monster in self.monster_list.items():
			# Highlight any targets
			alpha = monster.object.color[3]
			if monster in main['player'].targets:
				monster.object.color = [1, 0.6, 0.6, alpha]
			else:
				monster.object.color = [1, 1, 1, alpha]
			# Get rid of any dead guys
			if main['owns_combat'] and monster.hp <= 0:
				self.server.invoke("kill_monster", id)
		
			# This should get moved, but it will sit here for now
			if monster.action_set:
				self.play_animation(monster, "Idle", mode=1)
			
		# Our id so we can talk with the server
		id = main['client'].id
		
		if inputs:		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				
				if ("UsePower", "INPUT_CLICK") in inputs:
					self.use_power(main['player'], main['player'].powers.active.name)
				if ("NextPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_next_active()
				if ("PrevPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_prev_active()
				if ("UsePowerOne", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(0):
						self.use_power(main['player'], main['player'].powers.all[0])
				if ("UsePowerTwo", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(1):
						self.use_power(main['player'], main['player'].powers.all[1])
				if ("UsePowerThree", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(2):
						self.use_power(main['player'], main['player'].powers.all[2])
				if ("UsePowerFour", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(3):
						self.use_power(main['player'], main['player'].powers.all[3])
				if ("UsePowerFive", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(4):
						self.use_power(main['player'], main['player'].powers.all[4])
				if ("UsePowerSix", "INPUT_CLICK") in inputs:
					if main['player'].powers.has_power(5):
						self.use_power(main['player'], main['player'].powers.all[5])

				if ("TargetClosest", "INPUT_CLICK") in inputs:
					target = self.get_closest_target(main['player'], self.monster_list.values())
					if target:
						main['player'].targets = [target]
				if ("TargetPrevious", "INPUT_CLICK") in inputs:
					target = self.get_prev_target(main['player'].targets[0], list(self.monster_list.values()))
					if target:
						main['player'].targets = [target]
				if ("TargetNext", "INPUT_CLICK") in inputs:
					target = self.get_next_target(main['player'].targets[0], list(self.monster_list.values()))
					if target:
						main['player'].targets = [target]

				if ("Aim", "INPUT_ACTIVE") in inputs:
					if main['player'].powers.active.effect_shape == "SINGLE":
						self.camera = 'shoulder'
						main['ui_system'].mouse.visible = True
						
						# Enable camera pitch on mouse look
						dy = 0.5 - main['input_system'].mouse.position[1]
						cam_ori = Matrix(main['camera'].world_orientation)
						main['camera'].world_orientation = cam_ori * Matrix.Rotation(dy, 3, 'X')
						
						# Build a list of possible targets
						targets = self.monster_list.values()
						
						# Gather some info for the target searching
						distance = main['player'].powers.active.distance * UNIT_SIZE
						cam_vec = main['camera'].pivot.getAxisVect((0,0,-1))
						
						final_target = None
						final_factor = .5 #atan(1/distance) * distance
						for target in targets:
							target_vec = target.object.position - main['camera'].pivot.worldPosition.copy()
							target_vec_len = target_vec.length * UNIT_SIZE - 2
							if target_vec_len < distance:
								factor = cam_vec.angle(target_vec.normalized()) * target_vec_len
								if factor < final_factor:
									final_target = target
									final_factor = factor
									
						main['player'].targets = [final_target] if final_target else []
									
						
					else:					
						# Show the range of the active power
						power = main['player'].powers.active
						type = power.effect_shape
						size = power.distance
						
						if type in main['target_shapes']:
							main['target_shapes'][type].color = [1, 0, 0, 0.25]
							main['target_shapes'][type].scaling = Vector([size+HALF_UNIT_SIZE]*2 + [1])
							main['target_shapes'][type].visible = True
				else:
					main['ui_system'].mouse.visible = False

					
			result = self._handle_generic_input(main, inputs)
			if result: return result

	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		main['room'] = None
		
		# Put away the player's weapon
		main['player'].clear_right_hand()
						
	##########
	# Server
	##########
	
	@rpc(server_functions, "add_monster", str, int, str, float, float, float)
	def s_add_monster(self, main, client, monster, level, cid, x, y, z):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		
		if cid not in combat.monster_list:
			combat.monster_list[cid] = [MonsterLogic(None, Monster(monster), level), [x, y, z]]
			combat.monster_list[cid][0].cid = cid
			AiManager.add_agent(combat.monster_list[cid][0], "extern/cego/example_definitions/base.json", "spawn")
			self.clients.invoke("add_player", cid, [monster, level], 1, [x, y, z], None)
			self.clients.invoke("add_monster", client.combat_id, monster, cid, x, y, z)
			
			main['players'][cid] = combat.monster_list[cid][0]
		# else:
			# print("WARNING (add_monster): Monster id, '%s', has already been added, ignoring" % id)
		
	@rpc(server_functions, "kill_monster", str)
	def s_kill_monster(self, main, client, id):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		
		if id in combat.monster_list:
			monster, position = combat.monster_list[id]
			
			# Get rid of the monster
			self.clients.invoke("kill_monster", client.combat_id, id)
			self.clients.invoke("remove_player", id)
			
			# Now calculate some loot
			main['ground_item_counter'] += 1
			gid = main['ground_item_counter']
			
			item = random.choice([Items.Weapon, Items.Armor])
			item = item(random.choice(item.available_items), 1) # XXX level should be calculated from party level
			
			main['ground_items'][gid] = item
			self.clients.invoke("drop_item", gid, item, *position)
			
			del combat.monster_list[id]
			del main['players'][id]
		else:
			# print("WARNING (kill_monster): Monster id, '%s', not in list, ignoring" % id)
			return
			
		if len(combat.monster_list) < 1:
			self.clients.invoke("end_combat", client.combat_id)	
			del main['combats'][client.combat_id]
			self._next_state = "Default"
		
	@rpc(server_functions, "modify_health", str, float)
	def s_modify_health(self, main, client, id, amount):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		if id not in combat.monster_list: return
		
		monster = combat.monster_list[id][0]
		monster.hp += amount
		
		if monster.hp <= 0:
			self.s_kill_monster(main, client, id)
			
	@rpc(server_functions, "request_monsters")
	def request_monsters(self, main, client):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		if client.combat_id not in combat.monster_list: return
		
		for i, v in combat.monster_list.items():
			self.client.invoke("add_player", i, v[0].name, 1, v[1], None)
			self.client.invoke("add_monster", client.combat_id, v[0].name, i, *v[1])

	@rpc(server_functions, "add_hero")
	def s_add_hero(self, main, client):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		
		if client.id in combat.hero_list:
			# Already added, ignore
			return
			
		self.clients.invoke('add_hero', client.combat_id, client.id)
		
		for hero in combat.hero_list:
			self.client.invoke('add_hero', client.combat_id, hero)
	
	@rpc(server_functions, "rotate_monster", str, float, float, float)
	def s_rotate_monster(self, main, client, cid, x, y, z):
		self.clients.invoke("rotate_monster", cid, x, y, z)
		
	@rpc(server_functions, "position_monster", str, float, float, float)
	def s_position_monster(self, main, client, cid, x, y, z):
		combat = main['combats'].get(client.combat_id, None)
		if combat is None: return
		combat.monster_list[cid][1] = [x, y, z]
		self.clients.invoke("position_monster", cid, x, y, z)
		
	@rpc(server_functions, "add_node", "pickle")
	def s_add_node(self, main, client, node):
		combat = main['combats'].get(client.combat_id, None)
		combat.environment.append(node)
	
	@rpc(server_functions, "set_environment")
	def s_set_environment(selfself, main, client):
		combat = main['combats'].get(client.combat_id, None)
		AiManager.set_environment(combat.environment)
	
	def server_init(self, main):
		"""Initialize the server state"""
		self.main = main
		
		self.monster_id = 0
		# Setup Ai
		AiManager.set_controller(self)
		AiManager.set_extern_actions("Scripts.ai.actions")
		AiManager.set_extern_transitions("Scripts.ai.transitions")
		
		DefaultState.server_init(self, main)
		
	def server_run(self, main, client):
		"""Server-side run method"""
		self.main = main
		self.client = client
		
		# Run the ai if it is set up, else try to set it up
		if AiManager.get_environment():
			AiManager.run()
				
		if main['combats'].get(client.combat_id) == -1:
			main['combats'][client.combat_id] = Combat()
			
		DefaultState.server_run(self, main, client)
			
			
				
	##########
	# Other
	##########
	
	def _generate_encounter(self, deck, num_players=1):
		"""Generate an encounter by drawing cards from the encounter deck"""
		random.seed()
		
		no_brutes_soldiers = True
		monsters = []
		
		while no_brutes_soldiers:
			remaining = 4*num_players
			while remaining > 0:
				draw = random.choice(deck.cards)
				
				if draw['role'] in ('soldier', 'brute') and remaining >= 2:
					monsters.append(draw['monster'])
					no_brutes_soldiers = False
					remaining -= 2
				elif draw['role'] == 'minion':
					monsters.append(draw['monster'])
					remaining -= 1
				elif draw['role']:
					monsters.append(draw[0])
					remaining -= 4
				else:
					continue

		return monsters
	
	##########
	# Controller
	##########
	def deal_damage(self, character, strength, multiplier, type, delivery):
		self.modify_health(character, -int(strength*10*multiplier))
		
	def modify_health(self, character, amount):
		BaseController.modify_health(self, character, amount)
		
		for i, v in self.monster_list.items():
			if character == v:
				self.server.invoke("modify_health", i, amount)
				
				pos = character.object.position[:2]+(character.object.position[2]+2,)
				effect = effects.TextEffect(amount, pos, 90)
				self.add_effect(effect)
		
	def end_effect(self, id):
		self.main["effect_system"].remove(id)
		
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
		
		# Bump the range a bit to compensate for the first half "tile"
		# that the player occupies
		distance += HALF_UNIT_SIZE
		
		if not source:
			source = character.object.position

		targets = []
		
		if not target_types:
			return targets
			
		tlist = []
		if 'SELF' in target_types:
			tlist.append(self.main['player'])
		if 'ALLIES' in target_types:
			tlist.extend(self.hero_list.values() if character in self.hero_list.values() else self.monster_list.values())
		if 'ENEMIES' in target_types:
			tlist.extend(self.monster_list.values() if character in self.hero_list.values() else self.hero_list.values())
		
		if shape == 'SINGLE':
			ori_ivnt = character.object.get_orientation().inverted()
			for target in tlist:
				# Convert to local space
				v = target.object.position - source
				v = ori_ivnt * v
				
				# Now do a simple bounds check
				if v[1] < distance and abs(v[0]) < HALF_UNIT_SIZE:
					targets.append(target)
		elif shape == 'BURST':
			for target in tlist:
				
				# Do a simple distance check
				if (target.object.position - source).length < distance:
					targets.append(target)
		elif shape == 'CONE':
			pi_fourths = pi / 4
			for target in tlist:
			
				# Start with a simple distance check
				if (target.object.position - source).length < distance:
					
					# Now do an angle check
					v1 = character.object.forward_vector
					v2 = target.object.position - character.object.position
					
					angle = v1.angle(v2, 0)
					
					if angle < pi_fourths:
						targets.append(target)
				
		return targets		
	
	def spawn(self, character, position):
		if hasattr(self, 'clients'):	
			combat = self.main['combats'].get(self.client.combat_id, None)
			if combat and character.cid in combat.monster_list:
				combat.monster_list[character.cid][1] = position
			self.clients.invoke("position", character.cid, *position)
	
	def move(self, character, linear = (0,0,0) , angular = (0,0,0) , local = False):
		"""Handles linear and angular movement of a character"""
		
		# Move the character
		character.object.move(linear, min=[-50, -50, 0], max=[50, 50, 0], local=local)
		
		# Now handle rpcs
		self.server.invoke("rotate", character.id, *angular)
		self.server.invoke("position", character.id, *character.object.position)
		
	def reposition(self, character, position):
		character.object.position = position
		self.server.invoke("position", character.id, *character.object.position)
		
	def despawn(self, character):
		pass
	
	def attack(self, power, character, animation="1h Swing", multiplier=1):
		self.animate_weapon(character, animation)
		for target in self.get_targets(power, character):
			self.modify_health(target, -10*multiplier)
	
	def use_power(self, character, power):
		if isinstance(power, str):
			power = Power(power)
		if "SELF" in power.target_mask:
			power.use(self, character)
		else:
			character.auto_power = power
			character.auto_target = character.targets[0]
		
	def check_save(self, defender, def_stat, offender, off_stat):
		def_value = 0
		off_value = 0
		
		if offender == 'STATIC':
			off_value = 10
			if off_stat in defender.saving_throw_mods:
				off_value += defender.saving_throw_mods['off_stat']
				
			return random.randint(1, 20) >= off_value
			
		if off_stat.strip().lower()[:3] in ('str', 'con', 'dex', 'int', 'wis', 'cha'):
			off_value = offender.level//2 + getattr(offender, off_stat.strip().lower()[:3]+"_mod")
			off_value += random.randint(1, 20)
			
		if def_stat.strip().lower() in ('ac', 'fortitude', 'reflex', 'will'):
			def_value = getattr(defender, def_stat.strip().lower())
			
		
		return def_value >= off_value

	def _get_idle_animation(self, main):
		return '1h Idle'
		
	def _get_forward_animation(self, main):
		return '1h Walk'
