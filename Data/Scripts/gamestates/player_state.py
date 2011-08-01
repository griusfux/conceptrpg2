from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class PlayerState(DefaultState):
	"""A state for player screens"""
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		main['camera'].target = main['player'].object
		main['camera'].change_mode("shop", 30)
		
		self.last_layout = main['ui_system'].current_layout
		self.layout_loaded = False
		
		main['player_exit'] = False
		main['player_new_powers'] = []
		main['player_new_pp'] = self.main['player'].power_points
	
	def client_run(self, main):
		"""Client-side run method"""
		# Update the camera (this allows it to be animated)
		main['camera'].update()
		
		# If the camera is still transitioning, wait
		if main['camera']._transition_point != 0:
			return
		
		# If the inventory window isn't up yet, put it up
		if not self.layout_loaded:
			if main['overlay'] == "PlayerStats":
				main['ui_system'].load_layout("PlayerStatsLayout")
			elif main['overlay'] == "Inventory":
				main['ui_system'].load_layout("InventoryLayout")
			elif main['overlay'] == "Powers":
				main['ui_system'].load_layout("PowersLayout")
			self.layout_loaded = True
			
		# Get inputs
		inputs = main['input_system'].run()

		if ("Character", "INPUT_CLICK") in inputs:
			if main['overlay'] == "PlayerStats":
				return('', "POP")
			main['overlay'] = "PlayerStats"
			return("Player", "SWITCH")

		if ("Powers", "INPUT_CLICK") in inputs:
			if main['overlay'] == "Powers":
				return('', "POP")
			main['overlay'] = "Powers"
			return("Player", "SWITCH")

		if ("Inventory", "INPUT_CLICK") in inputs:
			if main['overlay'] == "Inventory":
				return('', "POP")
			main['overlay'] = "Inventory"
			return("Player", "SWITCH")
		
		if ("InGameMenu", "INPUT_CLICK") in inputs or main['player_exit']:
			for power in main['player_new_powers']:
				main['player'].powers.add(power, self)
			main['player'].power_points = main['player_new_pp']
			return('', 'POP')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['ui_system'].load_layout(self.last_layout)
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
		
		# Clean up main
		del main['player_exit']
		del main['player_new_powers']
		del main['player_new_pp']
