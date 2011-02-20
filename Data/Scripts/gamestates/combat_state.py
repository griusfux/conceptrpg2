# $Id$

from .base_state import BaseState, BaseController
from .default_state import DefaultState
from Scripts.packages import Monster
from Scripts.character_logic import MonsterLogic

import random
from math import degrees, sqrt, atan
from Scripts.ai.manager import Manager as AiManager
from Scripts.ai.state_machine import StateMachine as AiStateMachine
from Scripts.mathutils import Vector, Matrix

# Constants for grid generation
TILE_SIZE = 1
HALF_TILE_SIZE = TILE_SIZE/2.0
GRID_Z = 0.01

class CombatState(DefaultState, BaseController):		
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("combat")

		# Get room info
		self.room = CombatRoom(main['room'])
		
		# Place the monsters
		self.monster_list = []
		for monster in [Monster(i) for i in self._generate_encounter(main['dgen'].deck)]:
			# Load the monster
			main['engine'].load_library(monster)
		
			# Find a place to put the monster
			x = random.uniform(self.room.start_x+TILE_SIZE, self.room.end_x-TILE_SIZE)
			y = random.uniform(self.room.start_y+TILE_SIZE, self.room.end_y-TILE_SIZE)
					
			# Place the monster
			obj = main['engine'].add_object(monster.name, (x, y, GRID_Z))
			
			# Setup logic/ai
			logic = MonsterLogic(obj, monster)
			#([name, [actions], [entry_actions], [exit_actions], [(transition, target_state)]], [second_name, [actions], [entry_actions], [exit_actions], [(tran1, target1), (tran2, target2)]]
			logic.ai = AiStateMachine(logic, (["idle", ["seek"], [], [], [("hp_lt_zero", "death"),]], ["death", ["die"], [], [], []]))
			
			# Add the monster to the monster list
			self.monster_list.append(logic)
		
		# Initialize an ai manager
		# self.ai_manager = AiManager(self)
		
		# Set up the players
		self.hero_list = [main['player']]
		
		# If the player has a weapon, socket it
		if main['player'].inventory.weapon:
			weapon = main['player'].inventory.weapon
			main['engine'].load_library(weapon)
			obj = main['engine'].add_object('longsword')
			main['player'].set_right_hand(obj)
		self.camera = 'combat'
		self.last_camera = 'frankie'
			
		
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
		
		# See if we still need to be in combat
		if not self.monster_list:
			return ("Default", "SWITCH")

		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Targeting
		active_power = main['player'].powers.active
		range_type = active_power.range_type
		range_size = active_power.range_size
		if range_type == 'RANGED':
			# If the player already has targets, find out if they are valid
			if main['player'].targets:
				# Ranged can only have one target
				if len(main['player'].targets) > 1:
					main['player'].targets = []
				else:
					# The target must be in range
					if (main['player'].targets[0].object.position-main['player'].object.position).length > range_size:
						main['player'].targets = []
			else:
				target = None
				target_dist = range_size
				for monster in self.monster_list:
					dist = (monster.object.position-main['player'].object.position).length
					if dist < target_dist:
						target = monster
						target_dist = dist
				main['player'].targets = [target,] if target else []
		else:	
			mask = getattr(active_power, "mask", {'ENEMIES'})
			main['player'].targets = self.get_targets(main['player'], range_type, range_size, target_types=mask)		
		
			
		####	
		# ai
		
		#Dicision making
		# for monster in self.monster_list:
			# monster.target = [main['player']]
			# monster.actions = monster.ai.run()
			
		# Run the ai manager
		#self.ai_manager.run()
		
		# Maintain monsters
		for monster in self.monster_list:
			# Highlight any targets
			if monster in main['player'].targets:
				monster.object.color = [0.75, 0.15, 0.15, 1]
			else:
				monster.object.color = [1, 1, 1, 1]
			# Get rid of any dead guys
			if monster.hp <= 0:
				self.monster_list.remove(monster)
				xp_reward = monster.xp_reward/len(self.hero_list)
				for hero in self.hero_list:
					hero.xp += xp_reward
					main['player'].targets.remove(monster)
				monster.object.end()
			
		# Our id so we can talk with the server
		id = main['client'].id
		
		if inputs:
			if ("Inventory", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("inventory_overlay")
		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].powers.active.use(self, main['player'])
				if ("NextPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_next_active()
				if ("PrevPower", "INPUT_CLICK") in inputs:
					main['player'].powers.make_prev_active()				
				if ("Aim", "INPUT_ACTIVE") in inputs:
					if main['player'].powers.active.range_type == "RANGED":
						self.camera = 'shoulder'
						main['ui_system'].mouse.visible = True
						
						# Enable camera pitch on mouse look
						dy = 0.5 - main['input_system'].mouse.position[1]
						cam_ori = Matrix(main['camera'].world_orientation)
						main['camera'].world_orientation = cam_ori * Matrix.Rotation(dy, 3, 'X')
						
						# Build a list of possible targets
						targets = self.monster_list
						
						# Gather some info for the target searching
						distance = main['player'].powers.active.range_size * TILE_SIZE
						cam_vec = main['camera'].pivot.getAxisVect((0,0,-1))
						
						final_target = None
						final_factor = .5 #atan(1/distance) * distance
						for target in targets:
							target_vec = target.object.position - main['camera'].pivot.worldPosition.copy()
							target_vec_len = target_vec.length * TILE_SIZE - 2
							if target_vec_len < distance:
								factor = cam_vec.angle(target_vec.normalized()) * target_vec_len
								if factor < final_factor:
									final_target = target
									final_factor = factor
									
						main['player'].targets = [final_target] if final_target else []
									
						
					else:					
						# Show the range of the active power
						power = main['player'].powers.active
						point = main['player'].object.position
						# tiles = self._find_target_range(power.range_type, power.range_size, point)
						# for tile in tiles:
							# tile.color((1, 0, 0, 0.25))
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
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""

		pass
				
	##########
	# Other
	##########
	
	def _generate_encounter(self, deck, num_players=1):
		"""Generate an encounter by drawing cards from the encounter deck"""
		random.seed()
		
		no_brutes_soldiers = True
		monsters = []
		
		while no_brutes_soldiers:
			remaining = num_players
			while remaining > 0:
				draw = random.choice(deck.cards)
				
				if draw['role'] in ('soldier', 'brute'):
					monsters.extend([draw['monster'] for i in range(2)])
					no_brutes_soldiers = False
				elif draw['role'] == 'minion':
					monsters.extend([draw['monster'] for i in range(4)])
				elif draw['role']:
					monsters.append(draw[0])
				else:
					continue
					
				remaining -= 1

		return monsters
	
	##########
	# Controller
	##########
	
	def create_effect(self, effect_name, position, target=None, duration=0, delay=0, continuous=-1, **functions):
		id = self.main["effect_system"].create(effect_name, position, target, duration, delay, continuous, **functions)
		return id
		
	def add_effect(self, effect):
		id = self.main["effect_system"].add(effect)
		return id
		
	def end_effect(self, id):
		self.main["effect_system"].remove(id)
	
	def play_animation(self, character, animation, lock=0, mode=0):
		"""Instruct the character to play the animation
		
		character -- the charcter who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		character.add_lock(lock)
		character.object.play_animation(animation['name'], animation['start'], animation['end'], mode=mode)
		
		# self.server.invoke("anim", animation, 1, 20, 0, 0) # XXX should be done based on the supplied character
		
	def get_targets(self, character, type, _range, target_types={'ENEMIES'}, source=None):
		"""Get targets in a range
		
		character -- character using the power
		type -- the type of area (line, burst, etc)
		range -- the range to grab (integer)
		target_types -- which type of targets to grab (SELF, ALLIES, ENEMIES, etc)
		
		"""
		
		# Bump the range a bit to compensate for the first half "tile"
		# that the player occupies
		_range += HALF_TILE_SIZE
		
		if not source:
			source = character.object.position

		targets = []
		
		if not target_types:
			return targets
			
		tlist = []
		if 'SELF' in target_types:
			tlist.append(self.main['player'])
		if 'ALLIES' in target_types:
			tlist.extend(self.hero_list if character in self.hero_list else self.monster_list)
		if 'ENEMIES' in target_types:
			tlist.extend(self.monster_list if character in self.hero_list else self.hero_list)
		
		if type == 'MELEE':
			ori_ivnt = character.object.get_orientation().inverted()
			for target in tlist:
				# Convert to local space
				v = target.object.position - source
				v *= ori_ivnt
				
				# Now do a simple bounds check
				if v[1] < _range and abs(v[0]) < HALF_TILE_SIZE:
					targets.append(target)
		elif type == 'BURST':
			for target in tlist:
				
				# Do a simple distance check
				if (target.object.position - source).length < _range:
					targets.append(target)
				
		return targets		
	
	
	def move(self, id, character, linear = (0,0,0) , angular = (0,0,0) , local = False):
		"""Handles linear and angular movement of a character"""
		
		# Positions are not quite accurate in the movement blocking, also adapting
		# Rotate to the new method causes some problems.
		
		if 0:
			linear = Vector(linear)
			if linear.length > 0:
				# Convert to a world vector if local is true
				if local:
					angle = Vector((0,1,0)).angle(character.object.forward_vector)
					# linear.rotate(Euler((0, 0, angle)))
				
				# Ensure we are using a normalized vector
				linear.normalized()
				
				# Find the new position relative to the grid origin
				position = character.object.position - Vector(self.grid.origin) + linear
			
				# Convert to grid coordinates
				position = [int(i/TILE_SIZE) for i in position]
				position[1] *= -1
				
				# Get the tile that corresponds with the character's position
				tile = self.grid(position[0], position[1])
				
				if tile != None and tile.valid:
					# Convert to local space
					angle = character.object.forward_vector.angle(Vector((0,1,0)))
					# linear.rotate(Euler((0, 0, -angle)))
					
					# Apply the characters speed
					linear *= character.speed
				else:
					# The character can't move that way, so eliminate any movement in linear
					linear *= 0
		
		self.server.invoke("rotate", id, *angular)
		self.server.invoke("move", id, *linear)
			# print(position)
		

		# If the character has changed tiles, the tiles need to be updated to reflect this
		new_tile = self.grid.tile_from_point(character.object.position)
		if new_tile != character.tile:
			character.tile.fill(None)
			new_tile.fill(character)
			character.tile = new_tile
			
	def _get_idle_animation(self, main):
		return main['default_actions']['1h_idle']
		
	def _get_forward_animation(self, main):
		return main['default_actions']['1h_walk']
			
class CombatRoom:
	"""This class keeps track of room information"""
	
	def __init__(self, room):
		vert_list = [i for i in room.get_vertex_list() if i.z <= 0]
		
		# Find the smallest and largest x and y
		sx = lx = vert_list[0].x
		sy = ly = vert_list[0].y
		
		for vert in vert_list:
			if vert.x < sx:
				sx = vert.x
			elif vert.x > lx:
				lx = vert.x
				
			if vert.y < sy:
				sy = vert.y
			elif vert.y > ly:
				ly = vert.y
		
		# Record the size of the room
		self.width = lx - sx
		self.height = ly - sy
		
		self.start_x = sx
		self.start_y = sy
		
		self.end_x = lx
		self.end_y = ly
		
		# Find out how many tiles we need
		self.x_steps = int(round(self.width / TILE_SIZE))
		self.y_steps = int(round(self.height / TILE_SIZE))
	