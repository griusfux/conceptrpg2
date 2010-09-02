# $Id$

from .base_state import BaseState, BaseController
from Scripts.packages import Monster
from Scripts.character_logic import MonsterLogic

import random
import Scripts.Ai.machine as ai

# Constants for grid generation
TILE_SIZE = 1
GRID_Z = 0.01

# We don't need to bother subclassing DefaultState since we are going to mostly override
# everything anyways, and Python doesn't have abstract classes or interfaces.

class CombatState(BaseState, BaseController):		
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		print("Init combat...")
		
		main['ui_system'].load_layout("combat")
		
		# Generate the grid
		self.grid = CombatGrid(main['engine'], main['room'])

		# "Place" the player
		# player_tile = self.grid.tile_from_point(main['player'].object.position)
		# main['player'].object.position = player_tile.position
		
		# Place the monsters
		self.monster_list = []
		for monster in [Monster(i) for i in self._generate_encounter(main['dgen'].deck)]:
			# Load the monster
			main['engine'].load_library(monster)
		
			# Find a place to put the monster
			x = y = None
			while not x or not y:
				x = random.randrange(0, self.grid.x_steps)
				y = random.randrange(0, self.grid.y_steps)
				
				if not self.grid(x, y).valid:
					x = y = None
					
			# Place the monster
			tile = self.grid(x, y)
			obj = main['engine'].add_object(monster.name, tile.position)
			
			# Setup logic/ai
			logic = MonsterLogic(obj, monster)
			logic.ai = ai.Machine(monster.ai_keywords, monster.ai_start_state)
			
			tile.fill(logic)
			
			# Add the monster to the monster list
			self.monster_list.append(logic)
			
			
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# See if we still need to be in combat
		if not self.monster_list:
			main['client'].send('stateDefault')
			return ("Default", "SWITCH")

		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].object.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Keep our connection to the server alive
		val = main['client'].run()
		
		while val != None:
			cid, data = val
			
			# XXX This needs to be cleaned up
			if cid not in main['net_players']:
				root = main['engine'].add_object("NetEmpty")
				player = main['engine'].add_object("DarkKnightArm")
				player.gameobj.setParent(root.gameobj)
				main['net_players'][cid] = PlayerLogic(root)
			
			# Parse the inputs from the server
			try:
				for input in data:
					if input.startswith('mov'):
						input = input.replace('mov', '')
						main['net_players'][cid].object.move([float(i) for i in input.split('$')], min=[-50, -50, 0], max=[50, 50, 0])
					elif input.startswith('pos'):
						input = input.replace('pos', '')
						server_pos = [float(i) for i in input.split('$')]
						client_pos = main['net_players'][cid].object.position
						
						for i in range(3):
							if abs(server_pos[i]-client_pos[i]) > 1.0:
								client_pos[i] = server_pos[i]
							
						main['net_players'][cid].object.position = client_pos
					elif input.startswith('anim'):
						input = input.replace('anim', '')
						main['net_players'][cid].object.move((0, 0, 0))
						main['net_players'][cid].object.play_animation(input)
					elif input.startswith('to'):
						main['net_players'][cid].object.end()
						del main['net_players'][cid]
						print(cid, "timed out")
					elif input.startswith('dis'):
						main['net_players'][cid].object.end()
						del main['net_players'][cid]
						print(cid, "disconnected")
			except ValueError as e:
				print(e)
				print(val)
					
			val = main['client'].run()
			
		# Handle monster ai
		machine_input = {
					'combat_system': self,
					'foe_list': (main['player'],),
					'friend_list': self.monster_list
				}
				
		for monster in self.monster_list:
			machine_input['self'] = monster
			monster.ai.run(machine_input)
			
		# The message we will send to the server
		pos = main['player'].object.position
		msg = "pos%.4f$%.4f$%.4f " % (pos[0], pos[1], pos[2])
		
		if inputs:
			if ("SwitchCamera", "INPUT_ACTIVE") in inputs:
				main['engine'].set_active_camera(main['top_down_camera'])
				
			if ("Stats", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("stats")				
				
			if ("Inventory", "INPUT_CLICK") in inputs:
				main['ui_system'].toogle_overlay("inventory_overlay")
		
			# Only let the player do stuff while they are not "locked"
			if not main['player'].lock:
				# if ("Jump", "INPUT_ACTIVE") in inputs:
					# main['client'].send('stateDefault')
					# return ("Default", "SWITCH")
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].active_power.use(self, main['player'])

				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$5$0 "
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$-5$0 "
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					msg += "mov5$0$0 "
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					msg += "mov-5$0$0 "
					
				if 'mov' not in msg:
					target = self.grid.tile_from_point(main['player'].object.position)
					vec = main['player'].object.get_local_vector_to(target.position)
					vec[2] = 0
					vec = [i * main['player'].speed for i in vec]
					msg += "mov"+"$".join(["%.3f" % i for i in vec])
			
			# for row in self.grid.map:
				# for tile in row:
					# tile.color((0, 0, 0, 0))
			# Range check
			# tiles = self.get_targets("MELEE", 1)
			# for tile in tiles:
				# tile.color((1, 0, 0, 1))
				
	
		# Send the message
		main['client'].send(msg.strip())

	def client_cleanup(self, main):
		"""Cleanup the client state"""
		self.grid.end()

	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		
		print("\n\n\nCombat!\n\n\n")
		
		self.run = self.server_run
		
	def server_run(self, main, client):
		"""Server-side run method"""

		# Here we just need to broadcast the data to the other clients
		client.server.broadcast(client.id + " " + client.data)
		
		
		for input in client.data.split():
			if input.startswith("dis"):
				client.server.drop_client(client.id, "Disconnected")
			elif input.startswith("state"):
				input = input.replace('state', '')
				return (input, 'SWITCH')
				
	##########
	# Other
	##########
	
	def _generate_encounter(self, deck, num_players=1):
		"""Generate an encounter by drawing cards from the encounter deck"""
		
		random.seed()
		
		no_brutes_soldiers = True
		monsters = []
		
		while no_brutes_soldiers:
			while num_players > 0:
				draw = random.choice(deck.deck)
				
				if draw[1] in ('soldier', 'brute'):
					monsters.extend([draw[0] for i in range(2)])
					no_brutes_soldiers = False
				elif draw[1] == 'minion':
					monsters.extend([draw[0] for i in range(4)])
				elif draw[1]:
					monsters.append(draw[0])
				else:
					continue
					
				num_players -= 1
				
		return monsters
				
		
	def _find_target_range(self, type, _range, direction, point):
		# If the point passed in was a 2tuple, then add a z of GRID_SIZE to the end)
		if len(point) == 2:
			point += (GRID_SIZE,)
		# point = (point[0], point[1], point[2])
		tiles = []
		if type == 'MELEE':
			for i in range(_range):
				if direction == "+x":
					tiles.append(self.grid.tile_from_point((point[0]+TILE_SIZE*(i+1), point[1])))
				elif direction == "-x":
					tiles.append(self.grid.tile_from_point((point[0]-TILE_SIZE*(i+1), point[1])))
				elif direction == "+y":
					tiles.append(self.grid.tile_from_point((point[0], point[1]+TILE_SIZE*(i+1))))
				elif direction == "-y":
					tiles.append(self.grid.tile_from_point((point[0], point[1]-TILE_SIZE*(i+1))))
		elif type == 'RANGED':
			if _range == 'WEAPON':
				pass
			elif _range == 'SIGHT':
				pass
			else: # It's a number
				pass
		elif type == 'BLAST':
				pass
		elif type == 'BURST':
			radius = int(_range)+1
			y_vals = [sqrt((radius**2) - ((i+0.5)**2)) for i in range(radius)]
			for x in range(int(_range)+1):
				for y in range(int(round(y_vals[x]))):
					tiles.append(self.tile_from_point((point[0]+x*TILE_SIZE, point[1] + y*TILE_SIZE)))
			point = self.tile_from_point(point)
			next_quarter = [self.grid(curr.x - (curr.x-point.x)*2, curr.y) for curr in tiles if curr]
			tiles += next_quarter
			next_half = [self.grid(curr.x, curr.y - (curr.y-point.y)*2) for curr in tiles if curr]
			tiles += next_half
		elif type == 'wall':
				pass
		else:
			print("Invalid range type: %s" % type)

		# Remove invalid tiles
		while None in tiles:
			tiles.remove(None)
		return tiles
	
	##########
	# Controller
	##########
	
	def play_animation(self, character, animation, lock=0):
		"""Instruct the character to play the animation
		
		character -- the charcter who will play the animation
		animation -- the animation to play
		lock -- how long to lock for the animation
		
		"""
		
		character.add_lock(lock)
		self.main['client'].send('anim'+animation) # XXX should be done based on the supplied character
		
	def get_targets(self, type, range):
		"""Get targets in a range
		
		type -- the type of area (line, burst, etc)
		range -- the range to grab (integer)
		
		"""
		
		from mathutils import Vector # XXX Calling Blender stuff = bad
		from math import degrees
		
		targets = []
		
		# Find the direction
		vec = Vector(self.main['player'].object.forward_vector)
		angle = degrees(vec.angle(Vector((0, 1, 0))))
		
		if 0 < angle < 45:
			direction = "+y"
		elif 135 < angle < 180:
			direction = "-y"
		else:
			if vec[0] > 0:
				direction = "+x"
			else:
				direction = "-x"
		
		tiles = self._find_target_range(type, range, direction, self.main['player'].object.position)
		
		for tile in tiles:
			if tile.object:
				targets.append(tile.object)
				
		return targets		
				
	
# The following classes are for handling the combat grid
class CombatGrid:
	"""This object handles the grid aspect of combat, and is made up of CombatTile objects"""
	
	def __init__(self, Engine, room):
		vert_list = [i for i in room.get_vertex_list() if i.z <=0]
		
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
		x = lx - sx
		y = ly - sy
		self.origin = (sx, ly, GRID_Z)
		
		# Find out how many tiles we need
		self.x_steps = int(round(x / TILE_SIZE))
		self.y_steps = int(round(y / TILE_SIZE))
		
		# Create an empty 2D list/array to hold the grid
		self.map = [[None for i in range(self.y_steps)] for i in range(self.x_steps)]
		
		# Now fill the 2D list/array
		for x in range(self.x_steps):
			for y in range(self.y_steps):
				self.map[x][y] = CombatTile(Engine, x, y, (self.origin[0] + x, self.origin[1] - y, GRID_Z), room, self.x_steps, self.y_steps)
	
	def __call__(self, x, y):
		if x < 0 or y < 0:
			return None
			
		try:
			return self.map[x][y]
		except IndexError:
			return None
			
	def tile_from_point(self, point):
		"""Finds the tile that contains the point"""
		
		# Calculate the offset based on the distance from the origin
		x_off = abs(point[0] - self.origin[0])
		y_off = abs(point[1] - self.origin[1])
		
		# Convert the offset to tiles
		x = int(x_off/TILE_SIZE)
		y = int(y_off/TILE_SIZE)
		
		# Clamp the x, y to be in the grid
		if x > self.x_steps - 1:
			x = self.x_steps - 1
		elif x < 0:
			x = 0
			
		if y > self.y_steps - 1:
			y = self.y_steps - 1
		elif y < 0:
			y = 0
			
		# Return the tile
		return self(x, y)

	def end(self):
		for x in self.map:
			for y in x:
				y.end()
				
class CombatTile:
	"""The individual squares of the CombatGrid object"""
	
	def __init__(self, Engine, x, y, position, room, x_steps, y_steps):
		self.x = x
		self.y = y
		self.position = (position[0] + TILE_SIZE / 2, position[1] - TILE_SIZE / 2, position[2])
		self.valid = True
		self.object = None
		
		self.grid_color = Engine.add_object('GridColor', position)
		self.grid_color.color = [0, 0, 0, 0]
		
		# Check if the tile is in the room
		for vert in self.grid_color.get_vertex_list():
			hit_ob, hit_pos, hit_norm = Engine.ray_cast((vert.x, vert.y, vert.z + 1), (vert.x, vert.y, vert.z-1), self.grid_color)
			if not hit_ob or hit_ob != room:
				self.valid = False
				break
				
		# Check if anything is in the tile
		v1 = self.grid_color.get_vertex_list()[0]
		v2 = self.grid_color.get_vertex_list()[2]
		hit_ob, hit_pos, hit_norm = Engine.ray_cast((v1.x, v1.y, v1.z), (v2.x, v2.y, v2.z), self.grid_color)
		if hit_ob:
			self.valid = False
			
		# Place the appropriate tile based on validity
		self.grid_tile = Engine.add_object('GridTile', position) if self.valid else None
		# if self.valid:
			# self.grid_tile = Engine.add_object('GridTile', position)
		# else:
			# self.grid_tile = None
			# self.grid_color.set_color([1, 0, 0, 1])
			
	def color(self, color):
		self.grid_color.color = color
			
	def fill(self, object):
		"""'Fill' the tile with the given object, or empty it if object is none"""
		
		self.object = object
		
		if self.object:
			self.valid = False
		else:
			self.valid = True
		
	def end(self):
		"""A method to cleanup the tile when we are done"""
		if self.grid_tile:
			self.grid_tile.end()
		self.grid_color.end()
	