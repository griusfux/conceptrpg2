import bgui
from time import time

class Layout(bgui.Widget):
	def __init__(self, sys, name, use_mouse=False):
		bgui.Widget.__init__(self, sys, name, size=[1,1])
		
		sys.mouse.visible = use_mouse
		
	def update(self, main):
		# To be overridden
		pass
		
class StatsOverlay(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "stats_overlay")
		
		self.fps = bgui.Label(self, "fps", pt_size=42, pos=[0.05, .9])
		
	def update(self, main):
		self.fps.text = "%.2f fps" % main['engine'].fps
		
class InventoryOverlay(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "inventory_overlay")
		
		self.frame = bgui.Frame(self, "inv_frame", size=[0.25, 0.25], pos=[0.6, 0.4])

class DunGenLayout(Layout):
	
	def __init__(self, sys):
		
		Layout.__init__(self, sys, "dun_gen_layout")
		
		self.screen = bgui.Image(self, 'dun_gen_img', 'Textures/generatingw.png', size=[1, 1])
		
class DefaultStateLayout(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "default_state_layout")
		
		# Player data frame
		self.pframe = bgui.Frame(self, "ds_pframe", size=[0.25, 0.20], pos=[0.01, 0.01], sub_theme="HUD")
		self.player_name = bgui.Label(self.pframe, "ds_name", pt_size=34, pos=[0.05, 0.80])
		
		# HP
		self.hp_text = bgui.Label(self.pframe, "ds_hp", pt_size=16, pos=[0.10, 0.60])
		self.hp_bar = bgui.ProgressBar(self.pframe, "ds_hp_bar", size=[0.90, 0.03], pos=[0.05, 0.55],
									sub_theme='HP')#, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
									
		# EXP
		self.exp_text = bgui.Label(self.pframe, "ds_exp", pt_size=16, pos=[0.10, 0.40])
		self.exp_bar = bgui.ProgressBar(self.pframe, "ds_exp_bar", size=[0.90, 0.03], pos=[0.05, 0.35],
									sub_theme='Exp')#, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)		
		
		self.power = bgui.Label(self, "ds_power", pt_size=42, pos=[0.35, 0.15])
		self.lock_msg = bgui.Label(self, "lock_msg", pt_size=42, pos=[0.35, 0.05])
		
	def update(self, main):
		player = main['player']
		player.xp = 20
		self.player_name.text = player.name
		self.hp_text.text = "HP (%d/%d)" % (player.hp, player.max_hp)
		self.hp_bar._update_position([0.90*((player.max_hp/100)%1), 0.03], self.hp_bar._base_pos)
		self.hp_bar.percent = player.hp/player.max_hp
		
		self.exp_text.text = "EXP (%d/%d)" % (player.xp, player.xp+100-(player.xp%100))
		self.exp_bar.percent = player.xp/(player.xp + 100-(player.xp%100))
		
		self.power.text = player.powers.active.name
		self.lock_msg.text = "LOCKED: %s" % (main['player'].lock - time()) if main['player'].lock else ""
		
class CombatLayout(DefaultStateLayout):
	def __init__(self, sys):
		DefaultStateLayout.__init__(self, sys)