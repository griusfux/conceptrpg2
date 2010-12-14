import bgui
from .layouts import Layout

class LevelUpLayout(Layout):
	"""Layout for LevelUpState"""
	def __init__(self, sys):
		Layout.__init__(self, sys, "lvl_up_overlay", use_mouse=True)
		main_frame = bgui.Frame(self, "lvl_main_frame", aspect=(3/2), size=[0, .8],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED, sub_theme="HUD")
								# sub_theme="HUD")
		# main_frame.colors = [(0,0,0,0.5)]*4
		
		#########
		# Buttons
		self.lvl_btn = bgui.FrameButton(main_frame, "lvl_btn", text="Accept", pt_size=25,
										size=[.15, .06], pos=[.8, .02])
		self.lvl_btn.on_click = self.accept_on_click
		
		self.lvl_cancel = bgui.FrameButton(main_frame, "lvl_cancel", text="Cancel", pt_size=25,
										size=[.15, .06], pos=[.6, .02])
		self.lvl_cancel.on_click = self.cancel_on_click
		
		################
		# Abililty Frame
		ability_frame = bgui.Frame(main_frame, "lvl_ab_frame", size=[1, 0.4], pos=[0, 0.5])
		ability_frame.colors = [(0,0,0,0)]*4
		
		## Archetype Frame
		arch_frame = bgui.Frame(ability_frame, "lvl_arch_frame", size=[1/3, 1], pos=[0, 0])
		arch_frame.colors = [(1, 0, 0, 0)]*4
		
		## Abillity Points Frame
		points_frame = bgui.Frame(ability_frame, "lvl_points_frame", size=[1/3, 1], pos=[1/3, 0])
		points_frame.colors = [(0, 1, 0, 0)]*4
		
		## Ability Info Frame
		ab_info_frame = bgui.Frame(ability_frame, "lvl_ab_info_frame", size=[1/3, 1], pos=[2/3, 0])
		ab_info_frame.colors = [(0, 0, 1, 0)]*4
		
	def cancel_on_click(self, widget):
		self.main['level_exit'] = True
		
	def accept_on_click(self, widget):
		self.main['player'].unspent_levels.pop(0)
		self.main['level_exit'] = True
		
	def update(self, main):
		self.main = main