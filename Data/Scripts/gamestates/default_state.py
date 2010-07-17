# $Id$

class DefaultState:
	"""A combat system for when the player isn't actively engaged in an encounter"""
	
	def __init__(self, main, is_server=False):
		"""Constructor"""
		
		if is_server:
			self.server_init(main)
		else:
			self.client_init(main)
			
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['ui_system'].load_layout("passive_combat")
		self.run = self.client_run
		
	def server_init(self, main):
		"""Initialize the server state"""
		
		self.run = self.server_run
		
	def client_run(self, main):
		self._run(main)
		
	def server_run(self, client, main):
		client.server.broadcast(client.id + " " + client.data)
		
		for input in client.data.split():
			if input.startswith("dis"):
				client.server.drop_client(client.id, "Disconnected")
		
	def _run(self, main):
		"""A high-level run method"""
		
		# Reset the camera
		old_ori = main['3p_cam'].world_orientation
		main['3p_cam'].reset_orientation()
		main['player'].obj.set_orientation(old_ori, local=True)
		main['engine'].set_active_camera(main['3p_cam'])
		
		# Update the orientation values
		
		
		# Update the player's lock
		main['player'].update_lock()
		
		# Handles input
		inputs = main['input_system'].run()
		
		# Keep our connection to the server alive
		#main['client'].send("")
		val = main['client'].run()
		
		while val != None:
			cid, data = val
			
			if cid not in main['net_players']:
				player = main['engine'].add_object("DarkKnightArm")
				main['net_players'][cid] = PlayerLogic(player)
			
			try:
				for input in data:
					if input.startswith('mov'):
						input = input.replace('mov', '')
						main['net_players'][cid].obj.move([int(i) for i in input.split('$')], min=[-50, -50, 0], max=[50, 50, 0])
			except ValueError as e:
				print(e)
				print(val)
					
			val = main['client'].run()
		
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
					
					
				move = ""
				if ("MoveForward", "INPUT_ACTIVE") in inputs:
					move += "mov0$5$0 "
				if ("MoveBackward", "INPUT_ACTIVE") in inputs:
					move += "mov0$-5$0 "
				if ("MoveRight", "INPUT_ACTIVE") in inputs:
					move += "mov5$0$0 "
				if ("MoveLeft", "INPUT_ACTIVE") in inputs:
					move += "mov-5$0$0 "
					
				if not move:
					move = "mov0$0$0"
					
				main['client'].send(move.strip())
					
				#self._move_player(main['player'], inputs)
				
	def play_animation(self, char, action):
		char.obj.play_animation(action)
			
	def _move_player(self, player, inputs):
		"""Move the player"""
		
		moving = False
		
		if ("MoveForward", "INPUT_ACTIVE") in inputs:
			player.obj.move((0, 5, 0), min=[-50, -50, 0], max=[50, 50, 0])
			moving = True
		if ("MoveBackward", "INPUT_ACTIVE") in inputs:
			player.obj.move((0, -5, 0), min=[-50, -50, 0], max=[50, 50, 0])
			moving = True
		if ("MoveRight", "INPUT_ACTIVE") in inputs:
			player.obj.move((5, 0, 0), min=[-50, -50, 0], max=[50, 50, 0])
			moving = True
		if ("MoveLeft", "INPUT_ACTIVE") in inputs:
			player.obj.move((-5, 0, 0), min=[-50, -50, 0], max=[50, 50, 0])
			moving = True
			
		if moving:
			player.obj.play_animation("move")
		else:
			player.obj.play_animation("idle")
			player.obj.move((0, 0, 0))