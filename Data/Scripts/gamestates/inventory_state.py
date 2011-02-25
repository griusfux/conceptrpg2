from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class InventoryState(DefaultState):
	"""A state for the in-game menu"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		
		main['camera'].target = main['player'].object
		main['camera'].change_mode("shop", 60)
		
		self.last_layout = main['ui_system'].current_layout
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
			main['ui_system'].load_layout("inventory")
			self.layout_loaded = True
			
		# Get inputs
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs or \
			("Inventory", "INPUT_CLICK") in inputs:
			return('', 'POP')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['ui_system'].load_layout(self.last_layout)
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
