import bgui
import bge

from Scripts.ui.layouts import *

layouts = {
	"dun_gen": DunGenLayout,
	"passive_combat": PassiveCombatLayout,
	"combat": CombatLayout,
	
	"inventory_overlay": InventoryOverlay,
	"stats": StatsOverlay,
	}

class BlenderUISystem(bgui.System):
	"""A ui system to that can handle Blender events"""
	
	def __init__(self):
		# Init the system
		bgui.System.__init__(self)
		
		# All layouts will be a widget subclass, so we can just keep track of one widget
		self.layout = Layout(self, "none_layout")
		
		# We can also add 'overlay' layouts
		self.overlays = {}
		
		# Now we generate a dict to map BGE keys to bgui keys
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
		
	def load_layout(self, layout):
		self._widgets = {}
		self.layout = layouts[layout](self) if layout else Layout(self, "none_layout")
		
	def toogle_overlay(self, layout):
		if layout in self.overlays:
			self.remove_overlay(layout)
		else:
			self.add_overlay(layout)
		
	def add_overlay(self, layout):
		"""Add an overlay layout"""
		
		if layout in self.overlays:
			print("Overlay: %s, is already added" % layout)
			return
	
		self.overlays[layout] = layouts[layout](self.layout)
		
	def remove_overlay(self, layout):
		"""Remove an overlay layout by name"""
		
		if layout in self.overlays:
			self.layout._remove_widget(self.overlays[layout])
			del self.overlays[layout]
		else:
			print("WARNING: Overlay: %s was not found, nothing was removed" % layout)
		
	def run(self, main):
		"""A high-level method to be run every frame"""
		
		# Update the layout and overlays
		self.layout.update(main)
		
		for key, value in self.overlays.items():
			value.update(main)
		
		# Handle the mouse
		mouse = bge.logic.mouse
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
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw = [self.render]
