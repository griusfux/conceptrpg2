import bgui
from time import time

class Layout(bgui.Widget):
	def __init__(self, sys, name):
		bgui.Widget.__init__(self, sys, name, [1,1])
		
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
		
		self.hp = bgui.Label(self, "ds_hp", pt_size=42, pos=[0.05, 0.05])
		self.power = bgui.Label(self, "ds_power", pt_size=42, pos=[0.05, 0.15])
		self.lock_msg = bgui.Label(self, "lock_msg", pt_size=42, pos=[0.25, 0.05])
		
	def update(self, main):
		player = main['player']
		self.hp.text = "HP: %d/%d" % (player.hp, player.max_hp)
		self.power.text = player.powers.active.name
		self.lock_msg.text = "LOCKED: %s" % (main['player'].lock - time()) if main['player'].lock else ""
		
class CombatLayout(DefaultStateLayout):
	def __init__(self, sys):
		DefaultStateLayout.__init__(self, sys)