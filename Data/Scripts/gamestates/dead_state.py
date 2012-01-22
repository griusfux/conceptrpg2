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

from .combat_state import CombatState

class DeadState(CombatState):
	"""Dead gamestate"""

	client_functions = CombatState.client_functions.copy()
	server_functions = CombatState.server_functions.copy()
	
	ui_layout = "dead"
	
	##########
	# Client
	##########
	
	def client_init(self, main):
		"""Initialize the client state"""

		self.play_animation(main['player'], "Die")
		
	def client_run(self, main):
		"""Client-side run method"""
		
		player = main['player']
		inputs = main['input_system'].run()
		
		if inputs:
			if ("UsePower", "INPUT_CLICK") in inputs or \
				("Action", "INPUT_CLICK") in inputs:
				player.position = main['dgen'].start_position
				self.server.invoke("position", player.id, *player.position)
				player.hp = player.max_hp
				self.server.invoke("set_health", player.id, player.hp)
				main['dgen'].clear_barriers(main['room'])
				main['room'] = None
				return ("Default", "SWITCH")
			
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		pass
			
	##########
	# Server
	##########
		
	def server_init(self, main):
		"""Initialize the server state"""
		pass
		
	def server_run(self, main, client):
		"""Server-side run method"""
		pass
			
	def server_cleanup(self, main):
		"""Cleanup the server state"""
		pass

	##########
	# Other
	##########