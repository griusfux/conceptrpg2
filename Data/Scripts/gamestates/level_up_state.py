from .base_state import BaseState, BaseController
from Scripts.packages import *

class LevelUpState(BaseState, BaseController):
	"""A state to spend new level perks"""
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['ui_system'].load_layout("level_up")
		main['level_exit'] = False
	
	def client_run(self, main):
		"""Client-side run method"""
		# Get inputs
		inputs = main['input_system'].run()
		
		# Done leveling
		if main['level_exit']:
			for power in main['new_powers']:
				main['player'].powers.add(Power(power), self)
			main['player'].recalc_stats()
			return ("", "POP")
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		main['ui_system'].load_layout("default_state")
		del main['level_exit']
		del main['new_powers']
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)