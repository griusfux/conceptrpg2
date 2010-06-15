import bgui

class Layout(bgui.Widget):
	def __init__(self, sys, name):
		bgui.Widget.__init__(self, sys, name, [1,1])
		
	def update(self, main):
		# To be overridden
		pass

class DunGenLayout(Layout):
	
	def __init__(self, sys):
		
		Layout.__init__(self, sys, "dun_gen_layout")
		
		self.screen = bgui.Image(self, 'dun_gen_img', 'Textures/generatingw.png', size=[1, 1])
		
class PassiveCombatLayout(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "passive_combat_layout")
		
		self.hp = bgui.Label(self, "pc_hp", pt_size=42, pos=[0.05, 0.05])
		
	def update(self, main):
		player = main['player']
		self.hp.text = "HP: %d/%d" % (player.hp, player.max_hp)