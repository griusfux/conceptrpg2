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

import bgui
import bge
import collections

from Scripts.ui.layouts import *
from Scripts.ui.cgen_layouts import *
from Scripts.ui.tutorials import TutorialLayout
from Scripts.ui.shop_layout import *

layouts = {
	"cgen_select": CgenSelect,
	"cgen_name": CgenName,
	"cgen_race": CgenRace,
	"cgen_class": CgenClass,
	
	"title": TitleLayout,
	"ingame_menu": InGameMenuLayout,
	"inventory": InventoryLayout,
	"dun_gen": DunGenLayout,
	"default_state": DefaultStateLayout,
	"combat": CombatLayout,
	"dead": DeadLayout,
	"shop" : ShopLayout,
	
	"stats": StatsOverlay,
	"start_game_overlay": StartGameOverlay,
	"credits_overlay": CreditsOverlay
	}

class BlenderUISystem(bgui.System):
	"""A ui system to that can handle Blender events"""
	
	def __init__(self):
		# Init the system
		bgui.System.__init__(self, bge.logic.expandPath("//Scripts/ui/theme"))
		
		self.mouse = bge.logic.mouse
		
		# All layouts will be a widget subclass, so we can just keep track of one widget
#		self.current_layout = "none_layout"
#		self._change_layout = False
#		self.layout = Layout(self, self.current_layout)
		self.layout = None
		
		# We can also add 'overlay' layouts
		self.overlays = collections.OrderedDict()
		
		# Now we generate a dict to map BGE keys to bgui keys
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw.append(self.render)
		
	def load_layout(self, layout, state):
#		# Use a delayed loading of layouts, see run() for more info
#		self.current_layout = layout# if layout else "none_layout"
#		self._change_layout = True
#		self.current_layout = layout

		if self.layout:
			self._remove_widget(self.layout)

		if layout:
			if layout in globals():
				self.layout = globals()[layout](self, state)
			else:
				self.layout = layouts[layout](self, state)
		else:
			self.layout = None
		
	def toggle_overlay(self, layout):
		if layout in self.overlays:
			self.remove_overlay(layout)
		else:
			self.add_overlay(layout)
		
	def add_overlay(self, layout, state):
		"""Add an overlay layout"""
		
		if layout in self.overlays:
			print("Overlay: %s, is already added" % layout)
			return
	
		if layout in globals():
			self.overlays[layout] = globals()[layout](self, state)
		else:
			self.overlays[layout] = layouts[layout](self, state)
		
	def remove_overlay(self, layout):
		"""Remove an overlay layout by name"""
		
		if layout in self.overlays:
			self._remove_widget(self.overlays[layout])
			del self.overlays[layout]
			
			# Take care of mouse visibility
			use_mouse = self.layout.use_mouse
			if self.overlays:
				for overlay in self.overlays.values():
					use_mouse = overlay.use_mouse
			self.mouse.visible = use_mouse
		else:
			print("WARNING: Overlay: %s was not found, nothing was removed" % layout)
		
	def render(self):
		try:
			bgui.System.render(self)
		except:
			import traceback
			traceback.print_exc()
			bge.logic.getCurrentScene().post_draw.remove(self.render)
		
	def run(self, main):
		"""A high-level method to be run every frame"""
		
		# We use a delay loading of layouts so that the new layout's first update is called
		# immediately and in the same frame as creation. This gets rid of possible ui flickering
		# as layouts adjust themselves.
#		if self._change_layout:
#			if self.layout:
#				self._remove_widget(self.layout)
#			if self.current_layout:
#				if self.current_layout in globals():
#					self.layout = globals()[self.current_layout](self)
#				else:
#					self.layout = layouts[self.current_layout](self)
#			else:
#				self.layout = None
#			self._change_layout = False
#				
#		if not self.current_layout:
#			return

		if not self.layout:
			return
		
		# Update the layout and overlays
		self.layout.update(main)
		
		for key, value in self.overlays.items():
			value.update(main)
		
		# Handle the mouse
		mouse = self.mouse
		mouse_events = mouse.events
		
		pos = list(mouse.position[:])
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
		
		if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			mouse_state = bgui.BGUI_MOUSE_CLICK
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE
		else:
			mouse_state = bgui.BGUI_MOUSE_NONE
			
		self.update_mouse(pos, mouse_state)
		
		# Handle the keyboard
		keyboard = bge.logic.keyboard
		
		key_events = keyboard.events
		is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
					key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE
					
		for key, state in keyboard.events.items():
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)
