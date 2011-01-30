# $Id$

from .gamestates import *

# A dictionary to map strings to states
STATES = {
		"Default": DefaultState,
		"Title": TitleState,
		"InGameMenu": InGameMenuState,
		"CharacterCreation": CharacterCreationState,
		"DungeonGeneration": DungeonGenerationState,
		"Combat": CombatState,
		"Shop": ShopState,
		"LevelUp": LevelUpState,
		}
		


class GameStateManager:
	"""A class that manages game states"""
	
	def __init__(self, state, main, is_server=False):
		"""GameStateManager constructor"""
		
		# State stack
		self.states = [STATES[state](main, is_server)]
		
		# Server or client?		
		if is_server:
			self.run = self.server_run
		else:
			self.run = self.client_run
			
		self.is_server = is_server
		
	def client_run(self, main):
		"""Convenient client interface to the run method"""
		
		self._run(main)
		
	def server_run(self, main, client):
		"""Convenient server interface to the run method"""
		
		self._run(main, client)
		
	def _run(self, main, client=None):
		"""High level run method"""
		
		# We can't do anything with an empty stack
		if not self.states:
			raise RuntimeWarning("State stack is empty!")
			return
			
		# Run the top state on the stack and check it's return to see what to do next
		if client:
			val = self.states[0].run(main, client)
		else:
			val = self.states[0].run(main)
		
		if val:
			# Make sure the state is good
			if val[1] != 'POP' and val[0] not in STATES:
				RuntimeWarning(val[0]+" is not in the states list, ignoring")
				return
			
			if val[1] == 'SWITCH':
				# The state is done so remove it from the stack and transition to the new state
				self.states[0].cleanup(main)
				self.states.pop(0)
				self.states.insert(0, STATES[val[0]](main, self.is_server))
			elif val[1] == 'PUSH':
				# Suspend the current state and push the new state
				self.states.insert(0, STATES[val[0]](main, self.is_server))
			elif val[1] == 'POP':
				# Pop the state from the stack
				self.states[0].cleanup(main)
				self.states.pop(0)
			else:
				raise RuntimeError(val[1]+" is an invalid state flag!")
			