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

class TutorialState(DefaultState):
	"""A state to display tutorials"""
	
	ui_layout = None
	
	def client_init(self, main):
		"""Initialize the client state"""
		
		tutorial = main['tutorial_string']
		
		# Get the state ready to display the tutorial
		main['ui_system'].add_overlay("TutorialLayout", self)
		
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
		main['ui_system'].remove_overlay("TutorialLayout")
		
		# Reset the mouse position
		main['input_system'].mouse.position = (0.5, 0.5)
		
		# Clean up main
		del main['tutorial_exit']
		