from .base_state import BaseState

class TitleState(BaseState):
	"""A state for the title screen"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['action'] = ''
		main['ui_system'].load_layout("title")
	
	def client_run(self, main):
		"""Client-side run method"""
		
		if main['action']:
			action = main['action']
			
			if action == 'start':
				return ("CharacterCreation", "SWITCH")
			elif action == 'join':
				# Do the same as start for now
				return ("CharacterCreation", "SWITCH")
			elif action == 'options':
				print("Options menu isn't implemented yet")
			elif action == 'credits':
				print("Credits menu isn't implemented yet")
			elif action == 'exit':
				main['exit'] = True
			else:
				# Sanity check, should never happen
				print("Unsupported action:", action)

			main['action'] = ''
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		del main['action']
