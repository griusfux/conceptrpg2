from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class InGameMenuState(DefaultState):
	"""A state for the in-game menu"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['action'] = ''
		self.last_layout = main['ui_system'].current_layout
		main['ui_system'].load_layout("ingame_menu")
	
	def client_run(self, main):
		"""Client-side run method"""
		
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs:
			return('', 'POP')
		
		if main['action']:
			action = main['action']
			
			if action == 'game':
				return('', 'POP')
			elif action == 'options':
				print("Options not implemented yet")
			elif action == 'title':
				print("Return to Title not implemented yet")
			elif action == 'exit':
				main['exit'] = True
			else:
				# Sanity check, should never happen
				print("Unsupported action:", action)

			main['action'] = ''
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		del main['action']
		main['ui_system'].load_layout(self.last_layout)
		
		# Reset the mouse position
		# main['input_system'].mouse.position = (0.5, 0.5)