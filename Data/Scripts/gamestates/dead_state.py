from .combat_state import CombatState

class DeadState(CombatState):
	"""Dead gamestate"""

	client_functions = CombatState.client_functions.copy()
	server_functions = CombatState.server_functions.copy()
	
	ui_layout = "dead"
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Initialize the client state"""

		self.play_animation(main['player'], "Die")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		player = main['player']
		inputs = main['input_system'].run()
		
		if inputs:
			if ("UsePower", "INPUT_CLICK") in inputs or \
				("Action", "INPUT_CLICK") in inputs:
				player.position = main['dgen'].start_position
				self.server.invoke("position", player.id, *player.position)
				player.hp = player.max_hp
				self.server.invoke("set_health", player.id, player.hp)
				main['dgen'].clear_barriers(main['room'])
				main['room'] = None
				return ("Default", "SWITCH")
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		pass
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""
		pass
			
	def server_cleanup(self, main):
		"""Cleanup the server state"""
		pass

	##########
	# Other
	##########