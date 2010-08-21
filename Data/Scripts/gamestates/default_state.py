# $Id$

from Scripts.character_logic import PlayerLogic

class DefaultState:
	"""The default state for the game"""
	
	def __init__(self, main, is_server=False):
		"""Constructor"""
		
		if is_server:
			self.server_init(main)
		else:
			self.client_init(main)
			
	##########
	# Client
	##########
			
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("passive_combat")
		self.run = self.client_run
		
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
		#main['client'].send("")
		val = main['client'].run()
		
		while val != None:
			cid, data = val
			
			# XXX This needs to be cleaned up
			if cid not in main['net_players']:
				root = main['engine'].add_object("NetEmpty")
				player = main['engine'].add_object("DarkKnightArm")
				player.gameobj.setParent(root.gameobj)
				main['net_players'][cid] = PlayerLogic(root)
			
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
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		
		self.run = self.server_run
		
	def server_run(self, client, main):
		"""Server-side run method"""

		# Here we just need to broadcast the data to the other clients
		client.server.broadcast(client.id + " " + client.data)
		
		
		for input in client.data.split():
			if input.startswith("dis"):
				client.server.drop_client(client.id, "Disconnected")
				
	##########
	# Other
	##########
				
	def play_animation(self, char, action):
		char.obj.play_animation(action)
