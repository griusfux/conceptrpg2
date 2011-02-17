from .base_state import BaseState

class TitleState(BaseState):
	"""A state for the title screen"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['action'] = ''
		main['ui_system'].load_layout("title")
		
		self.current_overlay = ""
		main['start_game'] = False
	
	def client_run(self, main):
		"""Client-side run method"""
		
		if main['action']:
			action = main['action']
			
			if self.current_overlay:
				main['ui_system'].remove_overlay(self.current_overlay)
			
			if action == 'start':
				main['is_host'] = True
				self.current_overlay = "start_game_overlay"
			elif action == 'join':
				main['is_host'] = False
				self.current_overlay = "start_game_overlay"
			elif action == 'options':
				print("Options menu isn't implemented yet")
			elif action == 'credits':
				print("Credits menu isn't implemented yet")
			elif action == 'exit':
				main['exit'] = True
			else:
				# Sanity check, should never happen
				print("Unsupported action:", action)
				
			if self.current_overlay:
				main['ui_system'].add_overlay(self.current_overlay)

			main['action'] = ''
			
		if main['start_game']:
			if self.current_overlay:
				main['ui_system'].remove_overlay(self.current_overlay)
			return ("NetworkSetup", "SWITCH")
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		del main['action']
		del main['start_game']
