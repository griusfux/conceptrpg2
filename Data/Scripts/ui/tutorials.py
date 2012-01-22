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

#This file holds tutorials to be displayed to the player

import bgui
import Scripts.ui.custom_widgets as Custom
from .layouts import Layout

class TutorialLayout(Layout):
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "tutorial", state, use_mouse=True)
		self.tut = None
		
	def update(self, main):
		self.main = main
		if not self.tut:
			tutorial = main['tutorial_string']
			self.tut = globals().get(tutorial, None)
			
			if not self.tut:
				print("No tutorial found for %s." % tutorial)
				main['tutorial_exit'] = True
			else:
				self.tut = self.tut(self, self.state)
				self.tut.ok_btn.on_click = self.exit
				
	def exit(self, widget):
		self.main['tutorial_exit'] = True
			
			
class Tutorial(bgui.Image):
	def __init__(self, parent, state):
		bgui.Image.__init__(self, parent, "tut_frame",
										"Textures/ui/menu_background.png",
										1, [0, 0.7], [0,0],
										options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.title = bgui.Label(self, "title", sub_theme="Menu", pos=[0, 0.85],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		self.title.pt_size=60
		
		self.ok_btn = Custom.Button(self, "ok_btn", text="OK", pos=[0, 0.05],
									on_click=None,
									options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
class Controls(Tutorial):
	wasd = "The W, A, S, and D keys move the character forward, left, backward, and right (respectively)"
	cip = "The C, I, and P keys open the Character, Inventory, and Power menus (respectively)"
	mouse = "Mouse movement will change the direction the player is looking"
	def __init__(self, parent, state):
		Tutorial.__init__(self, parent, state)
		self.title.text = "Controls"
		
		bgui.Image(self, "wasd_p", "Textures/ui/tutorials/controls/wasd.png",
									1.4, [0, 0.15], [0.1, .65])

		bgui.Image(self, "cip_p", "Textures/ui/tutorials/controls/cip.png",
									175/60, [0, 0.075], [0.1, .5])
		
		bgui.TextBlock(self, "wasd_t", size=[0.5, 0.2],pos=[0.4, 0.6],
						sub_theme='Tutorial').text=self.wasd
		bgui.TextBlock(self, "cip_t", size=[0.5, 0.2], pos=[0.4, 0.4],
						sub_theme='Tutorial').text=self.cip
		bgui.TextBlock(self, "mouse_t", size=[0.5, 0.2], pos=[0.4, 0.2],
						sub_theme='Tutorial').text=self.mouse
		
class PowerPool(Tutorial):
	text1 = "Every player has a power pool with a fixed number of power points"
	text2 = "Every power has a power point cost that is modified by a player's affinities"
	text3 = "Powers can be freely added and removed from a power pool"
	def __init__(self, parent, state):
		Tutorial.__init__(self, parent, state)
		self.title.text = "Power Pool"
		
		bgui.Image(self, "text1_i", "Textures/ui/tutorials/power_pool/points.png",
									1, [0, 0.15], [0.135, .5])

		bgui.Image(self, "text2_i", "Textures/ui/tutorials/power_pool/add_remove.png",
									1, [0, 0.15], [0.135, .3])
		
		bgui.TextBlock(self, "text1", size=[0.5, 0.2], pos=[0.4, 0.6],
						sub_theme='Tutorial').text=self.text1
		bgui.TextBlock(self, "text2", size=[0.5, 0.2], pos=[0.4, 0.4],
						sub_theme='Tutorial').text=self.text2
		bgui.TextBlock(self, "text3", size=[0.5, 0.2], pos=[0.4, 0.2],
						sub_theme='Tutorial').text=self.text3

class Affinities(Tutorial):
	text1 = "Affinities decrease the cost of related powers"
	text2 = "Elemental affinities also influence character stats as follows:"
	text3 = "Death affects Arcane Damage\nStorm affects Physical Damage\nFire affects Accuracy\nHoly affects Arcane Defense\nEarth affects Physical Defense\nWater affects Reflex"
	def __init__(self, parent, state):
		Tutorial.__init__(self, parent, state)
		self.title.text = "Affinities"
		
		bgui.TextBlock(self, "text1", size=[0.8, 0.1], pos=[0.1, 0.65],
						sub_theme='Tutorial').text=self.text1
		bgui.TextBlock(self, "text2", size=[0.8, 0.1], pos=[0.1, 0.575],
						sub_theme='Tutorial').text=self.text2
		bgui.TextBlock(self, "text3", size=[0.8, 0.3], pos=[0.2, 0.25],
						sub_theme='Tutorial', pt_size=30).text=self.text3