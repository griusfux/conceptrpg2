from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class ShopState(DefaultState):
	"""A state to handle shopping from a shopkeeper"""
	
	ui_layout = None
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['shop_exit'] = False
		
		main['camera'].target = main['shop_spot']
		main['camera'].change_mode("shop", 60)
		self.layout_loaded = False
	
	def client_run(self, main):
		"""Client-side run method"""
		main['camera'].update()
		
		# If the camera is still transitioning, wait
		if main['camera']._transition_point != 0:
			return
		
		# If the shop window isn't up yet, put it up
		if not self.layout_loaded:
			main['ui_system'].load_layout("shop", self)
			self.layout_loaded = True
		
		# Get inputs
		inputs = main['input_system'].run()
		
		# Exiting the shop
		if ("Action", "INPUT_CLICK") in inputs or main['shop_exit']:
			return ("", "POP")
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['camera'].target = main['player'].object
		del main['shop_exit']
		
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main):
		"""Server-side run method"""
		pass
			
	def server_cleanup(self, main):
		"""Cleanup the server state"""
		pass