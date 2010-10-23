import bgui
from time import time

class Layout(bgui.Widget):
	def __init__(self, sys, name, use_mouse=False):
		bgui.Widget.__init__(self, sys, name, [1,1])
		
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

class CharacterCreationLayout(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "char_creation_layout", use_mouse=True)
		
		self.races = []
		self.classes = []
		
		self.race_idx = self.class_idx = 0
		
		# Name
		
		self.name_lbl = bgui.Label(self, "name", text="Name", pos=[0, .9], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		bgui.Label(self, "race_lbl", text="Choose your race", pos=[0, 0.85], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		# Race
		
		self.race_frame = bgui.Frame(self, "races", size=[1, .33], pos=[0, .50])
		self.race_frame.colors = [[0, 0, 0, 0] for i in range(4)]
		
		# replace these with images
		self.race_scroll = [
			bgui.Frame(self.race_frame, "race_scroll_left", size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			bgui.Frame(self.race_frame, "race_scroll_right", size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			]
			
		self.race_scroll[0].on_click = self.race_left
		self.race_scroll[1].on_click = self.race_right
		
		# Class
		
		bgui.Label(self, "class_lbl", text="Choose your class", pos=[0, 0.45], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		self.class_frame = bgui.Frame(self, "classes", size=[1, .33], pos=[0, .1])
		self.class_frame.colors = [[0, 0, 0, 0] for i in range(4)]
		
		# replace these with images
		self.class_scroll = [
			bgui.Frame(self.class_frame, "class_scroll_left", size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			bgui.Frame(self.class_frame, "class_scroll_right", size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			]
			
		self.class_scroll[0].on_click = self.class_left
		self.class_scroll[1].on_click = self.class_right
		
		# Go!
		start_btn = bgui.FrameButton(self, "start_btn", text="Start", pt_size=24, size=[0.1, 0.05], pos=[.85, .05])
		start_btn.on_click = self.start
		
	def update(self, main):
		self.main = main
	
		if not self.races:
			self.update_races()
		if not self.classes:
			self.update_classes()

	def update_races(self):		
		if self.race_idx+3 > len(self.main['races']):
			max = len(self.main['races'])
		else:
			max = self.race_idx+3
			
		if self.race_idx < 0:
			self.race_id

		self.races = []
	
		for i in range(self.race_idx, max):
			self.races.append(bgui.Image(self.race_frame, "race"+str(i),
			self.main['races'][i].image, aspect=(0.75), size=[1, .9], pos=[.18+(.25*(i-self.race_idx)), 0],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY))
		
	def update_classes(self):		
		if self.class_idx+3 > len(self.main['classes']):
			max = len(self.main['classes'])
		else:
			max = self.class_idx+3
			
		if self.class_idx < 0:
			self.class_idx = 0

		self.classes = []
	
		for i in range(self.class_idx, max):
			self.classes.append(bgui.Image(self.class_frame, "class"+str(i),
			self.main['classes'][i].image, aspect=(0.75), size=[1, .9], pos=[.18+(.25*(i-self.class_idx)), 0],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY))
				
			
	def race_left(self, parent):
		self.race_idx -= 1
		self.update_races()
		
	def race_right(self, parent):
		self.race_idx += 1
		self.update_races()
		
	def class_left(self, parent):
		self.class_idx -= 1
		self.update_classes()
		
	def class_right(self, parent):
		self.class_idx += 1
		self.update_classes()
		
	def start(self, parent):
		self.main['creation_done'] = True
		
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