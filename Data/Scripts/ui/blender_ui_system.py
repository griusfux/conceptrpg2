import bgui
import bge

from Scripts.ui.layouts import *

layouts = {
	"dun_gen": DunGenLayout,
	"passive_combat": PassiveCombatLayout
	}

class BlenderUISystem(bgui.System):
	"""A ui system to that can handle Blender events"""
	
	def __init__(self):
		# Init the system
		bgui.System.__init__(self)
		
		# All layouts will be a widget subclass, so we can just keep track of one widget
		self.layout = Layout(self, "none_layout")
		
		# Now we generate a dict to map BGE keys to bgui keys
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
		
	def load_layout(self, layout):
		self._widgets = {}
		self.layout = layouts[layout](self) if layout else Layout(self, "none_layout")
		
	def run(self, main):
		"""A high-level method to be run every frame"""
		
		# Update the layout
		self.layout.update(main)
		
		# Handle the mouse
		mouse = bge.logic.mouse
		
		pos = list(mouse.position[:])
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
		
		if (bge.events.LEFTMOUSE, bge.logic.KX_INPUT_JUST_ACTIVATED) in mouse.events:
			mouse_state = bgui.BGUI_MOUSE_CLICK
		elif (bge.events.LEFTMOUSE, bge.logic.KX_INPUT_JUST_RELEASED) in mouse.events:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif (bge.events.LEFTMOUSE, bge.logic.KX_INPUT_ACTIVE) in mouse.events:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE
		else:
			mouse_state = bgui.BGUI_MOUSE_NONE
			
		self.update_mouse(pos, mouse_state)
		
		# Handle the keyboard
		keyboard = bge.logic.keyboard
		is_shifted = (bge.events.LEFTSHIFTKEY, bge.logic.KX_INPUT_ACTIVE) in keyboard.events or \
					(bge.events.RIGHTSHIFTKEY, bge.logic.KX_INPUT_ACTIVE) in keyboard.events
					
		for key, state in keyboard.events:
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw = [self.render]
