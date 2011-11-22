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
		
		bgui.TextBlock(self, "wasd_t", size=[0.5, 0.2], pos=[0.4, 0.6]).text=self.wasd
		bgui.TextBlock(self, "cip_t", size=[0.5, 0.2], pos=[0.4, 0.4]).text=self.cip
		bgui.TextBlock(self, "mouse_t", size=[0.5, 0.2], pos=[0.4, 0.2]).text=self.mouse
		
class PowerPool(Tutorial):
	text1 = "Every player has a power pool with a fixed number of power points"
	text2 = "Every power has a power point cost that is modified by a player's affinities"
	text3 = "Powers can be freely added and removed from a power pool"
	def __init__(self, parent, state):
		Tutorial.__init__(self, parent, state)
		self.title.text = "Power Pool"
		
		bgui.Image(self, "text1_i", "Textures/ui/tutorials/controls/wasd.png",
									1.4, [0, 0.15], [0.1, .65])

		bgui.Image(self, "text2_i", "Textures/ui/tutorials/controls/cip.png",
									175/60, [0, 0.075], [0.1, .5])
		
		bgui.TextBlock(self, "text1", size=[0.5, 0.2], pos=[0.4, 0.6]).text=self.text1
		bgui.TextBlock(self, "text2", size=[0.5, 0.2], pos=[0.4, 0.4]).text=self.text2
		bgui.TextBlock(self, "text3", size=[0.5, 0.2], pos=[0.4, 0.2]).text=self.text3

class Affinities(Tutorial):
	text1 = "Affinities decrease the cost of related powers"
	text2 = "Elemental affinities also influence character stats as follows:"
	text3 = "Death\t\t->\tArcane Damage\nStorm\t\t->\tPhysical Damage\nFire\t\t->\tAccuracy\nHoly\t\t->\tArcane Defense\nEarth\t\t->\tPhysical Defense\nWater\t\t->\tReflex"
	def __init__(self, parent, state):
		Tutorial.__init__(self, parent, state)
		self.title.text = "Affinities"
		
		bgui.TextBlock(self, "text1", size=[0.8, 0.1], pos=[0.1, 0.65]).text=self.text1
		bgui.TextBlock(self, "text2", size=[0.8, 0.1], pos=[0.1, 0.575]).text=self.text2
		bgui.TextBlock(self, "text3", size=[0.6, 0.3], pos=[0.5, 0.25]).text=self.text3