from .default_state import DefaultState

class TutorialState(DefaultState):
	"""A state to display tutorials"""
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		tutorial = main['tutorial_string']
		print("Displaying %s tutorial" % tutorial)
		
		# Get the state ready to display the tutorial
		self.last_layout = main['ui_system'].current_layout
		main['ui_system'].load_layout("TutorialLayout")
		
		main['tutorial_exit'] = False
		
		# Set the mouse on the OK button
		main['input_system'].mouse.position = (0.5, 0.78)
		
	def client_run(self, main):
		"""Client-side run method"""
		
		# Get inputs
		inputs = main['input_system'].run()
		
		if main['tutorial_exit'] or ("InGameMenu", "INPUT_CLICK") in inputs:
			return('', "POP")
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['ui_system'].load_layout(self.last_layout)
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
		
		# Clean up main
		print("Tutorial Cleanup")
		del main['tutorial_exit']
		