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

from .base_state import BaseState

class TitleState(BaseState):
	"""A state for the title screen"""
	
	ui_layout = "title"
	
	def client_init(self, main):
		"""Intialize the client state"""
		main['action'] = ''
		main['ui_system'].load_layout("title", self)
		
		self.current_overlay = ""
		main['start_game'] = False
		main['overlay_done'] = False
		
		main['engine'].play_bgm('Heroic Age')
	
	def client_run(self, main):
		"""Client-side run method"""
		
		if main['action']:
			action = main['action']
			
			if self.current_overlay:
				main['ui_system'].remove_overlay(self.current_overlay)
				self.current_overlay = ""
			
			if action == 'start':
				main['is_host'] = True
				self.current_overlay = "start_game_overlay"
			elif action == 'join':
				main['is_host'] = False
				self.current_overlay = "start_game_overlay"
			elif action == 'options':
				print("Options menu isn't implemented yet")
			elif action == 'credits':
				self.current_overlay="credits_overlay"
			elif action == 'exit':
				main['exit'] = True
			else:
				# Sanity check, should never happen
				print("Unsupported action:", action)
				
			if self.current_overlay:
				main['ui_system'].add_overlay(self.current_overlay, self)

			main['action'] = ''
			
		if main['start_game']:
			if self.current_overlay:
				main['ui_system'].remove_overlay(self.current_overlay)
				self.current_overlay = ""
			return ("NetworkSetup", "SWITCH")
			
		if main['overlay_done']:
			main['ui_system'].remove_overlay(self.current_overlay)
			self.current_overlay = ""
			main['overlay_done'] = False

		
	def client_cleanup(self, main):
		"""Cleanup the client state"""
		del main['action']
		del main['start_game']
		del main['overlay_done']
