from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class InventoryState(DefaultState):
	"""A state for the in-game menu"""
	
	ui_layout = None
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		main['camera'].target = main['player'].object
		main['camera'].change_mode("shop", 30)
		
		self.layout_loaded = False
	
	def client_run(self, main):
		"""Client-side run method"""
		# Update the camera (this allows it to be animated)
		main['camera'].update()
		
		# If the camera is still transitioning, wait
		if main['camera']._transition_point != 0:
			return
		
		# If the inventory window isn't up yet, put it up
		if not self.layout_loaded:
			main['ui_system'].load_layout("PlayerStatsLayout", self)
			self.layout_loaded = True
			
		# Get inputs
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs or \
			("Inventory", "INPUT_CLICK") in inputs:
			return('', 'POP')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
