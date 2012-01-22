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

from .default_state import DefaultState

# We subclass DefaultState so we still have RPCs for networking
class InventoryState(DefaultState):
	"""A state for the in-game menu"""
	
	ui_layout = None
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		main['camera'].target = main['player'].object
		main['camera'].change_mode("shop", 30)
		
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
			main['ui_system'].load_layout("PlayerStatsLayout", self)
			self.layout_loaded = True
			
		# Get inputs
		inputs = main['input_system'].run()
		
		if ("InGameMenu", "INPUT_CLICK") in inputs or \
			("Inventory", "INPUT_CLICK") in inputs:
			return('', 'POP')
		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
