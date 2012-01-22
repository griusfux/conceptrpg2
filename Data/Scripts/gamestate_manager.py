# Copyright (C) 2011-2012 Mitchell Stokes and Daniel Stokes

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .gamestates import *

# A dictionary to map strings to states
STATES = {
		"Default": DefaultState,
		"Title": TitleState,
		"InGameMenu": InGameMenuState,
		"NetworkSetup": NetworkSetupState,
		"CharacterCreation": CharacterCreationState,
		"CharacterSelect": CharacterSelectState,
		"DungeonGeneration": DungeonGenerationState,
		"Combat": CombatState,
		"Shop": ShopState,
		"Player": PlayerState,
		"Inventory": InventoryState,
		"Dead": DeadState,
		"Tutorial" : TutorialState,
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
			
		last_idx = len(self.states) - 1
		# Run the all the states on the queue and check the return values to see what to do next
		for idx, state in enumerate(self.states[:]): # Use a copy of self.states so we can remove items from it if we need to
			
			# Only the last state is "active"
			state.suspended = idx != last_idx
			
			if client:
				val = state.run(main, client)
			else:
				val = state.run(main)
			
			if val:
				# Make sure the state is good
				if val[1] != 'POP' and val[0] not in STATES:
					RuntimeWarning(val[0]+" is not in the states list, ignoring")
					return
				
				if val[1] == 'SWITCH':
					# The state is done so remove it from the "queue" and transition to the new state
					state.cleanup(main)
					self.states.remove(state)
					self.states.insert(idx, STATES[val[0]](main, self.is_server))
					if not self.is_server:
						main['ui_system'].load_layout(self.states[idx].ui_layout, self.states[idx])
				elif val[1] == 'PUSH':
					# Suspend the current state and enqueue the new state
					state = STATES[val[0]](main, self.is_server)
					self.states.append(state)
					
					if not self.is_server and state.ui_layout:
						main['ui_system'].add_overlay(state.ui_layout, state)
				elif val[1] == 'POP':
					# Remove the state from the "queue"
					state.cleanup(main)
					if not self.is_server and state.ui_layout:
						main['ui_system'].remove_overlay(state.ui_layout)
					self.states.remove(state)
				else:
					raise RuntimeError(val[1]+" is an invalid state flag!")
				