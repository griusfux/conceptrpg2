#This file holds tutorials to be displayed to the player

import bgui
import Scripts.ui.custom_widgets as Custom
from .layouts import Layout

class TutorialLayout(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "tutorial", use_mouse=True)
		self.tut = None
#		self.parent_ = parent
		
	def update(self, main):
		self.main = main
		if not self.tut:
			tutorial = main['tutorial_string']
			self.tut = globals().get(tutorial, None)
			
			if not self.tut:
				print("No tutorial found for %s." % tutorial)
				main['tutorial_exit'] = True
			else:
				self.tut = self.tut(self)
				self.tut.ok_btn.on_click = self.exit
				
	def exit(self, widget):
		self.main['tutorial_exit'] = True
			
			
class Tutorial(bgui.Image):
	def __init__(self, parent):
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
	def __init__(self, parent):
		Tutorial.__init__(self, parent)
		self.title.text = "Controls"
		
		bgui.Image(self, "wasd_p", "Textures/ui/tutorials/controls/wasd.png",
									1.4, [0, 0.15], [0.1, .65])

		bgui.Image(self, "cip_p", "Textures/ui/tutorials/controls/cip.png",
									175/60, [0, 0.075], [0.1, .5])
		
		bgui.TextBlock(self, "wasd_t", size=[0.5, 0.2], pos=[0.4, 0.6]).text=self.wasd
		bgui.TextBlock(self, "cip_t", size=[0.5, 0.2], pos=[0.4, 0.4]).text=self.cip
		bgui.TextBlock(self, "mouse_t", size=[0.5, 0.2], pos=[0.4, 0.2]).text=self.mouse
