# $Id$

from .base_state import BaseState

# Constants for grid generation
TILE_SIZE = 1
GRID_Z = 0.01

# We don't need to bother subclassing DefaultState since we are going to mostly override
# everything anyways, and Python doesn't have abstract classes or interfaces.

class CombatState(BaseState):		
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		print("Init combat...")
		
		main['ui_system'].load_layout("combat")
		self.run = self.client_run
		
		# Generate the grid
		self.grid = CombatGrid(main['engine'], main['room'])		
		
	def client_run(self, main):
		"""Client-side run method"""

		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].obj.set_orientation(old_ori, local=True)
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
						main['net_players'][cid].obj.move([int(i) for i in input.split('$')], min=[-50, -50, 0], max=[50, 50, 0])
					elif input.startswith('pos'):
						input = input.replace('pos', '')
						server_pos = [float(i) for i in input.split('$')]
						client_pos = main['net_players'][cid].obj.get_position()
						
						for i in range(3):
							if abs(server_pos[i]-client_pos[i]) > 1.0:
								client_pos[i] = server_pos[i]
							
						main['net_players'][cid].obj.set_position(client_pos)
					elif input.startswith('to'):
						main['net_players'][cid].obj.end()
						del main['net_players'][cid]
						print(cid, "timed out")
					elif input.startswith('dis'):
						main['net_players'][cid].obj.end()
						del main['net_players'][cid]
						print(cid, "disconnected")
			except ValueError as e:
				print(e)
				print(val)
					
			val = main['client'].run()
			
		# The message we will send to the server
		pos = main['player'].obj.get_position()
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
				if ("Jump", "INPUT_ACTIVE") in inputs:
					main['client'].send('stateDefault')
					return ("Default", "SWITCH")
				if ("UsePower", "INPUT_ACTIVE") in inputs:
					target = main['player']
					main['player'].active_power.use(self, main['player'], target)

				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$5$0 "
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					msg += "mov0$-5$0 "
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					msg += "mov5$0$0 "
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					msg += "mov-5$0$0 "
					
				if 'mov' not in msg:
					msg += "mov0$0$0"
	
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
	
	# -----
	
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
		origin = (sx, ly, GRID_Z)
		
		# Find out how many tiles we need
		self.x_steps = int(round(x / TILE_SIZE))
		self.y_steps = int(round(y / TILE_SIZE))
		
		# Create an empty 2D list/array to hold the grid
		self.map = [[None for i in range(self.y_steps)] for i in range(self.x_steps)]
		
		# Now fill the 2D list/array
		for x in range(self.x_steps):
			for y in range(self.y_steps):
				self.map[x][y] = CombatTile(Engine, x, y, (origin[0] + x, origin[1] - y, GRID_Z), room, self.x_steps, self.y_steps)
				
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
		self.obj = None
		
		self.grid_color = Engine.add_object('GridColor', position)
		self.grid_color.set_color([0, 0, 0, 0])
		
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
			
	def end(self):
		if self.grid_tile:
			self.grid_tile.end()
		self.grid_color.end()
	