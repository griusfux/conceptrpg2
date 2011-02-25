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
		
class InventoryLayout(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "inventory_overlay")
		
		self.frame = bgui.Frame(self, "inv_frame", size=[0.6, 0.8], pos=[0.1, 0.1], sub_theme="HUD")
		
		# Player stats
		self.stats_frame = bgui.Frame(self.frame, "st_frame", size=[0.33, 0.5], pos=[0, 0.5], sub_theme="Transp")
		self.pname = bgui.Label(self.stats_frame, "pname", text="Name:", pos=[0.05, 0.9])
		self.prace = bgui.Label(self.stats_frame, "prace", text="Race:", pos=[0.05, 0.8])
		self.pclass = bgui.Label(self.stats_frame, "pclass", text="Class:", pos=[0.05, 0.7])
		self.plvl = bgui.Label(self.stats_frame, "plvl", text="Level:", pos=[0.05, 0.6])
		self.pxp = bgui.Label(self.stats_frame, "pxp", text="Exp:", pos=[0.05, 0.5])
		self.xpnl = bgui.Label(self.stats_frame, "xpnl", text="Exp to Next Level:", pos=[0.05, 0.4])
		
		# Player abilities
		self.ab_frame = bgui.Frame(self.frame, "ab_frame", size=[0.34, 0.5], pos=[0.33, 0.5], sub_theme="Transp")
		self.str = bgui.Label(self.ab_frame, "str", text="Str:", pos=[0.05, 0.9])
		self.con = bgui.Label(self.ab_frame, "con", text="Con:", pos=[0.05, 0.8])
		self.dex = bgui.Label(self.ab_frame, "dex", text="Dex:", pos=[0.05, 0.7])
		self.int = bgui.Label(self.ab_frame, "int", text="Int:", pos=[0.05, 0.6])
		self.wis = bgui.Label(self.ab_frame, "wis", text="Wis:", pos=[0.05, 0.5])
		self.cha = bgui.Label(self.ab_frame, "cha", text="Cha:", pos=[0.05, 0.4])
		
		# Player defenses
		self.def_frame = bgui.Frame(self.frame, "def_frame", size=[0.33, 0.5], pos=[0.67, 0.5], sub_theme="Transp")
		self.ac = bgui.Label(self.def_frame, "ac", text="AC:", pos=[0.05, 0.9])
		self.fortitude = bgui.Label(self.def_frame, "Fortitude:", pos=[0.05, 0.8])
		self.reflex = bgui.Label(self.def_frame, "Reflex:", pos=[0.05, 0.7])
		self.will = bgui.Label(self.def_frame, "Will:", pos=[0.05, 0.6])
		
		# Player inventory
		self.inv_frame = bgui.Frame(self.frame, "inv_frame", size=[0.5, 0.5], pos=[0, 0], sub_theme="Transp")
		bgui.Label(self.inv_frame, "inv_header", text="Inventory", pt_size=42, pos=[0.05, 0.85])
		
		# Player equipment
		self.eq_frame = bgui.Frame(self.frame, "eq_frame", size=[0.5, 0.5], pos=[0.5, 0], sub_theme="Transp")
		self.weapon = bgui.Label(self.eq_frame, "weapon", text="Weapon:", pos=[0.05, 0.9])
		self.armor = bgui.Label(self.eq_frame, "armor", text="Armor:", pos=[0.05, 0.8])
		self.shield = bgui.Label(self.eq_frame, "shield", text="Shield:", pos=[0.05, 0.7])
		
		self.items = None
		
	def update(self, main):
		player = main['player']
		
		# Player stats
		self.pname.text = "Name: "+player.name
		self.prace.text = "Race: "+player.race.name
		self.pclass.text = "Class: "+player.player_class.name
		self.plvl.text = "Level: "+str(player.level)
		self.pxp.text = "Exp: "+str(player.xp)
		self.xpnl.text = "Exp to Next Level: "+str(player.next_level)
		
		# Player abilities
		self.str.text = "Str:\t"+str(player.str_ab)
		self.con.text = "Con:\t"+str(player.con_ab)
		self.dex.text = "Dex:\t"+str(player.dex_ab)
		self.int.text = "Int:\t"+str(player.int_ab)
		self.wis.text = "Wis:\t"+str(player.wis_ab)
		self.cha.text = "Cha:\t"+str(player.cha_ab)
		
		# Player defenses
		self.ac.text = "AC: "+str(player.ac)
		self.fortitude.text = "Fortitude: "+str(player.fortitude)
		self.reflex.text = "Reflex: "+str(player.reflex)
		self.will.text = "Will: "+str(player.will)
		
		# Player inventory
		if not self.items:
			item_str = "\n".join([item.name for item in main['player'].inventory])

			self.items = bgui.TextBlock(self.inv_frame, "inv_items", text=item_str, size=[0.96, 0.80], pos=[0.1, 0])
			
		# Player equipment
		self.weapon.text = "Weapon: "+player.weapon.name
		self.armor.text = "Armor: "+player.armor.name
		self.shield.text = "Shield: "+player.shield.name
			
class TitleLayout(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "title_layout", use_mouse=True)
		
		# Background image
		self.splash = bgui.Image(self, "title_splash", "Textures/TitleSplash.png", size=[1, 1], pos=[0, 0])
		
		# Menu entries
		self.menu = [
				bgui.Label(self.splash, "title_start", text="Start Game", pos=[0.05, 0.210]),
				bgui.Label(self.splash, "title_join", text="Join Game", pos=[0.05, 0.170]),
				bgui.Label(self.splash, "title_options", text="Options", pos=[0.05, 0.130]),
				bgui.Label(self.splash, "title_credits", text="Credits", pos=[0.05, 0.090]),
				bgui.Label(self.splash, "title_exit", text="Exit", pos=[0.05, 0.050])
			]
			
		for i in self.menu:
			i.on_hover = self.menu_hover
			i.on_click = self.menu_click
		
		
	def update(self, main):
		self.main = main
		for i in self.menu: i.pt_size=26
		
	def menu_hover(self, widget):
		widget.pt_size = 32
		
	def menu_click(self, widget):
		widget.pt_size = 32
		self.main['action'] = widget.name.split('_')[-1]
		
class StartGameOverlay(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "start_game_overlay", use_mouse=True)
		
		# Background frame
		self.frame = bgui.Frame(self, "sgo_frame", size=[.33, .66], pos=[0.30, 0.05],
			sub_theme='HUD')
			
		self.user = bgui.TextInput(self.frame, "sgo_user", prefix="Username: ",
				size=[0.5, 0.07], pos=[0.05, 0.8], text="User")
				
		self.ip = bgui.TextInput(self.frame, "sgo_ip", prefix="Server IP: ",
				size=[0.5, 0.07], pos=[0.05, 0.7], text="localhost")
				
		self.port = bgui.TextInput(self.frame, "sgo_port", prefix="Server Port: ",
				size=[0.5, 0.07], pos=[0.05, 0.6], text="9999")

		# "Go" button
		self.go_button = bgui.FrameButton(self.frame, "sgo_go", text="",
			size=[0.2, 0.075], pos=[0.75, 0.05])
		self.go_button.on_click = self.button_click
			
	def update(self, main):
		self.main = main
		if not self.go_button.text:
			self.go_button.text = "Start" if main['is_host'] else "Join"
		if main['is_host'] and self.ip.visible:
			self.ip.visible = False
			
	def button_click(self, widget):
		self.main['user'] = self.user.text
		self.main['addr'] = (self.ip.text, int(self.port.text))
		self.main['start_game'] = True

class CreditsOverlay(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "credits_overlay", use_mouse=True)
		
		# Background frame
		self.frame = bgui.Frame(self, "co_frame", size=[0.33, 0.66], pos=[0.30, 0.05],
			sub_theme='HUD')
			
		# Credits text pulled from a file
		with open('../credits.txt') as f:
			self.block = bgui.TextBlock(self.frame, "co_block", text=f.read().replace("\t", "    "),
				size=[0.95, 0.65], pos=[0.05, 0.3])
		
		# "Go" button
		self.go_button = bgui.FrameButton(self.frame, "sgo_go", text="Done",
			size=[0.2, 0.075], pos=[0.75, 0.05])
		self.go_button.on_click = self.button_click
		
	def update(self, main):	
		self.main = main
		
	def button_click(self, widget):
		self.main['overlay_done'] = True

class InGameMenuLayout(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "ingame_menu", use_mouse=True)
		
		# Background frame
		self.frame = bgui.Frame(self, "igm_frame", size=[.25, .50], sub_theme='HUD',
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
				
		# Menu entries
		self.menu = [
				bgui.FrameButton(self.frame, "img_game", text="Return to Game", size=[0.8, 0.125], pos=[0, 0.775], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX),
				bgui.FrameButton(self.frame, "img_options", text="Options", size=[0.8, 0.125], pos=[0, 0.550], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX),
				bgui.FrameButton(self.frame, "img_title", text="Return to Title", size=[0.8, 0.125], pos=[0, 0.325], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX),
				bgui.FrameButton(self.frame, "igm_exit", text="Save and Exit", size=[0.8, 0.125], pos=[0, 0.1], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		]
		
		for i in self.menu:
			i.on_click = self.menu_click
			
	def update(self, main):
		self.main = main
		
	def menu_click(self, widget):
		self.main['action'] = widget.name.split('_')[-1]
		
class DunGenLayout(Layout):
	
	def __init__(self, sys):
		
		Layout.__init__(self, sys, "dun_gen_layout")
		
		# A timer for animation
		self.timer = 1
		
		# Background image
		bgui.Image(self, "dun_gen_bg", "Textures/ui/character select/bg_color.png", size=[1, 1], pos=[0, 0])
		
		# Grid we will place everything on
		self.grid = bgui.Image(self, "dun_gen_grid", "Textures/ui/character select/grid.png", aspect=(4/3), size=[1,1],
					options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		# Tell the user what's going on
		self.label = bgui.Label(self.grid, 'dun_gen_lbl', text="Generating dungeon",
								pt_size=60, pos=[0,0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		# An elipsis for animatino
		self.elipsis = bgui.Label(self.label, 'dun_gen_elps', text="",
								pt_size=60, pos=[1, 0],)
					
		# self.screen = bgui.Image(self, 'dun_gen_img', 'Textures/generatingw.png', size=[1, 1])
		
	def update(self, main):
		self.timer += 1
		
		if self.timer % 15 == 0:
			self.elipsis.text += " ."
			
		if self.timer == 59:
			self.elipsis.text = ""
			self.timer = 1
			
		
class DefaultStateLayout(Layout):
	def __init__(self, sys):
		Layout.__init__(self, sys, "default_state_layout")
		
		# Player data frame
		self.pframe = bgui.Frame(self, "ds_pframe", aspect=(5/2), size=[0.25, 0.20], pos=[0.01, 0.01], sub_theme="HUD")
		self.player_name = bgui.Label(self.pframe, "ds_name", pt_size=34, pos=[0.05, 0.80])
		
		# HP
		self.hp_text = bgui.Label(self.pframe, "ds_hp", pt_size=16, pos=[0.10, 0.60])
		self.hp_bar = bgui.ProgressBar(self.pframe, "ds_hp_bar", size=[0.90, 0.03], pos=[0.05, 0.55],
									sub_theme='HP')#, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
									
		# EXP
		self.exp_text = bgui.Label(self.pframe, "ds_exp", pt_size=16, pos=[0.10, 0.40])
		self.exp_bar = bgui.ProgressBar(self.pframe, "ds_exp_bar", size=[0.90, 0.03], pos=[0.05, 0.35],
									sub_theme='Exp')#, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)		
		
		# Level Up Message Frame
		self.mframe = bgui.Frame(self, "ds_mframe", aspect=8, size=[0, 0.05], pos=[0.75, 0.01])
		self.mframe.colors = [(0,0,0,0,)]*4
		self.mimg = bgui.Image(self.mframe, "ds_mimg", "Textures/ui/hex_tile.png", aspect=1,
								size=[0, 1],)
		self.mtext = bgui.Label(self.mframe, "ds_mtext", pt_size=22, pos=[.15, .2])
		
		
		# Locked message
		self.lock_msg = bgui.Label(self, "lock_msg", pt_size=42, pos=[0.35, 0.90])
		
	def update(self, main):
		player = main['player']
		self.player_name.text = "%s (Lvl %d)" % (player.name, player.level)
		self.hp_text.text = "HP (%d/%d)" % (player.hp, player.max_hp)
		self.hp_bar._update_position([0.90*min(player.max_hp/100, 1), 0.03], self.hp_bar._base_pos)
		self.hp_bar.percent = player.hp/player.max_hp
		
		self.exp_text.text = "EXP (%d/%d)" % (player.xp, player.next_level)#player.xp+100-(player.xp%100))
		self.exp_bar.percent = (player.xp-player.last_level)/(player.next_level-player.last_level+1)
		
		self.lock_msg.text = "LOCKED: %s" % (main['player'].lock - time()) if main['player'].lock else ""
		
		if not self.mtext.text:
			key = main['input_system'].event_to_string("LevelUp")
			key = key[:-3].title()
			self.mtext.text = "Press %s to level up!" % key
		if main['player'].unspent_levels:
			self.mframe.visible = True
		else:
			self.mframe.visible = False
		
class CombatLayout(DefaultStateLayout):
	def __init__(self, sys):
		DefaultStateLayout.__init__(self, sys)	
		
		# Power Bar
		self.power_imgs = []
		self.power_bar_selection=-1
		self.power_frame = bgui.Frame(self, "ds_sframe", aspect=8, size=[0.1, 0.1], pos=[0.35, 0.01])
		self.power_frame.colors = [(0, 0, 0, 0)]*4
		
	def update_powerbar(self, main):
		hex = 	{"AT_WILL" : "Textures/ui/hex_tile_blue.png",
				 "ENCOUNTER" : "Textures/ui/hex_tile_green.png",
				 "DAILY" : "Textures/ui/hex_tile_red.png"}
	
		psys = main['player'].powers
		powers = psys.all
	
		# Clear the old images
		for i in self.power_imgs:
			self.power_frame._remove_widget(i)
		self.power_imgs = []
	
		# Create new images
		for i in range(min(8, len(powers))):
			# Background
			bg = "Textures/ui/hex_tile_gray.png" if powers[i].spent else hex[powers[i].usage]
			img = bgui.Image(self.power_frame, "sbg"+str(i), bg,
							 size=[1/8, 1], pos=[(1/8)*i, 0.5 if i == psys.active_index else 0])
							 
			# Label
			if i == psys.active_index:
				lbl = bgui.Label(img, "slbl"+str(i), powers[i].name,
								pt_size=20 if i == psys.active_index else 14,
								pos=[0, 1 if i == psys.active_index else -0.05],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			
			# Power icon
			img_name = powers[i].open_image()
			simg = bgui.Image(img, powers[i].name, img_name, size=[1, 1], pos=[0, 0])
			powers[i].close_image()
			self.power_imgs.append(img)
								
		self.power_bar_selection = psys.active_index
		
	def update (self, main):
		DefaultStateLayout.update(self, main)
		
		if self.power_bar_selection != main['player'].powers.active_index:
			self.update_powerbar(main)
			