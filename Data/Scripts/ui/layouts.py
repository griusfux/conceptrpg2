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
from time import time
from Scripts.ui.custom_widgets import *
from Scripts.character_logic import PlayerLogic, ELEMENT_COLOR
from Scripts.packages import Power, Race, Class

class Layout(bgui.Widget):
	def __init__(self, sys, name, state, use_mouse=False):
		bgui.Widget.__init__(self, sys, name, size=[1,1])
		self.use_mouse = use_mouse
		sys.mouse.visible = use_mouse
		self.state = state
		
	def update(self, main):
		# To be overridden
		pass
		
class StatsOverlay(Layout):
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "stats_overlay", state)
		
		self.fps = bgui.Label(self, "fps", pt_size=42, pos=[0.05, .9])
		
	def update(self, main):
		self.fps.text = "%.2f fps" % main['engine'].fps
		
class PlayerStatsLayout(Layout):
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "player_stats_overlay", state, use_mouse=True)
		
		self.mframe = bgui.Image(self, "1x1_frame", "Textures/ui/menu_background.png",
								 aspect=1, size=[0,.9],	sub_theme="HUD",
								 options=BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.mframe.position = [.675-self.mframe.size[0]/parent.size[0], self.mframe.position[1]]
		
		#=======================================================================
		# Character Frame
		#=======================================================================
		self.cframe = bgui.Frame(self.mframe, "char_frame", size=[0.35, 0.3],
								pos=[0.05, 0.65], sub_theme="Menu")
		self.pname = bgui.Label(self.cframe, "pname", text="", sub_theme="Title", pos=[0, 0.9],
							options=BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.race = bgui.Label(self.cframe, "element", text="", sub_theme="Menu", pos=[0.03, 0.8])
		self.classinfo = bgui.Label(self.cframe, "raceclass", text="", sub_theme="Menu", pos=[0.03, 0.73])
		# HP
		self.hp_text = bgui.Label(self.cframe, "ds_hp", sub_theme="Menu", pos=[0.03, 0.6])
		self.hp_bar = bgui.ProgressBar(self.cframe, "ds_hp_bar", size=[0.90, 0.05], pos=[0.03, 0.50],
									sub_theme='HP')
									
		# EXP
		self.exp_text = bgui.Label(self.cframe, "ds_exp", sub_theme="Menu", pos=[0.03, 0.4])
		self.exp_bar = bgui.ProgressBar(self.cframe, "ds_exp_bar", size=[0.90, 0.05], pos=[0.03, 0.30],
									sub_theme='Exp')
		
		#=======================================================================
		# Stats Frame
		#=======================================================================
		self.sframe = bgui.Frame(self.mframe, "stat_frame", size=[0.50, 0.3],
								pos=[0.45, 0.65], sub_theme="Menu")

		self.pstatlbl = bgui.Label(self.sframe, "pstatlbl", text="Player Stats", sub_theme="Title", pos=[0, 0.9],
							options=BGUI_DEFAULT|bgui.BGUI_CENTERX)

		self.physdlbl = bgui.Label(self.sframe, 'physdlbl', text='Physical Damage:', sub_theme="Menu", pos=[0.03, 0.80])
		self.physd = bgui.Label(self.sframe, 'physd', sub_theme='Menu', pos=[0.4, 0.80])
		self.arcdlbl = bgui.Label(self.sframe, 'arcdlbl', text='Arcane Damage:', sub_theme="Menu", pos=[0.03, 0.73])
		self.arcd = bgui.Label(self.sframe, 'arcd', sub_theme='Menu', pos=[0.4, 0.73])
		self.accylbl = bgui.Label(self.sframe, 'accylbl', text='Accuracy:', sub_theme="Menu", pos=[0.03, 0.66])
		self.accy = bgui.Label(self.sframe, 'accy', sub_theme='Menu', pos=[0.4, 0.66])
		self.physdeflbl = bgui.Label(self.sframe, 'physdeflbl', text='Physical Defense:', sub_theme="Menu", pos=[0.53, 0.80])
		self.physdef = bgui.Label(self.sframe, 'physdef', sub_theme='Menu', pos=[0.91, 0.80])
		self.arcdeflbl = bgui.Label(self.sframe, 'arcdeflbl', text='Arcane Defense:', sub_theme="Menu", pos=[0.53, 0.73])
		self.arcdef = bgui.Label(self.sframe, 'arcdef', sub_theme='Menu', pos=[0.91, 0.73])
		self.reflexlbl = bgui.Label(self.sframe, 'reflexlbl', text='Reflex:', sub_theme="Menu", pos=[0.53, 0.66])
		self.reflex = bgui.Label(self.sframe, 'reflex', sub_theme='Menu', pos=[0.91, 0.66])
		
		#=======================================================================
		# Affinities Frame
		#=======================================================================
		self.aframe = bgui.Frame(self.mframe, "aff_frame", size=[0.35, 0.55],
								pos=[0.05, 0.05], sub_theme="Menu")

		self.afflbl = bgui.Label(self.aframe, "afflbl", text="Affinities", sub_theme="Title", pos=[0, 0.9],
							options=BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.affinities = AffinityWidget(self.aframe, size=[0.9, 0.85], pos=[0, 0.03])

		#=======================================================================
		# Description Frame
		#=======================================================================
		self.dframe = bgui.Frame(self.mframe, "desc_frame", size=[0.50, 0.55],
								pos=[0.45, 0.05], sub_theme="Menu")
		self.can_btn = Button(self.dframe, "revert_btn", text="CANCEL",
							on_click=self.cancel_click, pos=[0.3, 0.05])
		self.acc_btn = Button(self.dframe, "accept_btn", text="ACCEPT",
							on_click=self.accept_click, pos=[0.65, 0.05])
		
		
	def update(self, main):
		self.main = main
		
		player = main['player']
		
		# Update player info
		self.pname.text = player.name+"  [Level %d]"%player.level
		if not self.race.text:
			# Labels here should remain static, and don't need to be updated
			self.race.text = player.race.name
			self.classinfo.text = "%s (%s/%s)" % (player.player_class.subclass[player.element], player.player_class.name, player.element.title())
		if self.affinities.affinities is None:
			self.affinities.affinities = player.affinities.copy()
			self.affinities.affinity_points = player.affinity_points
			self.affinities.delivery_points = player.delivery_points
				
		# Update affinity info
		self.affinities.update(player)

		self.hp_text.text = "HP (%d/%d)" % (player.hp, player.max_hp)
		self.hp_bar._update_position([0.90*min(player.max_hp/100, 1), 0.03], self.hp_bar._base_pos)
		self.hp_bar.percent = player.hp/player.max_hp
		
		self.exp_text.text = "EXP (%d/%d)" % (player.xp, player.next_level)
		self.exp_bar.percent = (player.xp-player.last_level)/(player.next_level-player.last_level+1)
		
		self.physd.text = str(player.physical_damage)
		self.arcd.text = str(player.arcane_damage)
		self.accy.text = str(player.accuracy)
		self.physdef.text = str(player.physical_defense)
		self.arcdef.text = str(player.arcane_defense)
		self.reflex.text = str(player.reflex)
		
	def accept_click(self, widget):
		player = self.main['player']
		player.affinities = self.affinities.affinities.copy()
		player.affinity_points = self.affinities.affinity_points
		player.delivery_points = self.affinities.delivery_points
		
		player.recalc_stats()
		self.main['player_exit'] = True
		
	def cancel_click(self, widget):
		self.main['player'].recalc_stats()
		self.main['player_exit'] = True
		
class InventoryLayout(Layout):
	class ItemCellRenderer():
		def __init__(self, listbox, inventory):
			self.frame = bgui.Frame(listbox, "frame", size=[1, 0.0625],
									sub_theme="Submenu")
			self.label = bgui.Label(self.frame, "label", pos=[.05,.2],
								sub_theme="Menu", options=bgui.BGUI_DEFAULT)
			
			self.listbox = listbox
			self.inventory = inventory
			
		def render_item(self, item):
			color = [[0,0,0,0]] * 4
			if item == self.listbox.selected:
				color = [[0,0,0,.1]] * 4
				
			self.frame.colors = color
			
			player = self.inventory.main['player']
			if self.inventory.selection == "weapons":
				pitem = player.weapon
			elif self.inventory.selection == "armor":
				pitem = player.armor
			else:
				pitem = None
			self.label.text = item.name

			if item == pitem:
				self.label.color = [1, 1, 1, 1]
			else:
				self.label.color = self.label.theme['Color']
			return self.frame
			
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "inventory_overlay", state, use_mouse=True)
		
		self.mframe = bgui.Image(self, "1x1_frame", "Textures/ui/menu_background.png",
								 aspect=1, size=[0,.9],	sub_theme="HUD",
								 options=BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.mframe.position = [.675-self.mframe.size[0]/parent.size[0],
								self.mframe.position[1]]
		
		self.lframe = bgui.Frame(self.mframe, "list_frame", size=[0.4, 0.8], 
								pos=[0.05, 0.1], sub_theme="Menu")
		
		self.lbox = bgui.ListBox(self.lframe, "list_box", size=[1, 0.9])
		self.lbox.renderer = self.ItemCellRenderer(self.lbox, self)
		
		self.type_buttons = {}
		self.type_labels = {}
		self.selection = "weapons"
		self.old_selection = ""
		for i, type in enumerate(["weapons", "armor", "acc.", "misc."]):
			self.type_buttons[type] = bgui.Frame(self.lframe, type, size=[0.25, 0.1],
													pos=[0.25*i, 0.9])
			self.type_buttons[type].colors = [[0,0,0,0.1]] * 4
			self.type_buttons[type].border = 1
			self.type_buttons[type].border_color = [0.55, 0.29, 0.16, 0.7]
			self.type_buttons[type].on_click = self.selection_click
			self.type_labels[type] = bgui.Label(self.type_buttons[type], type+'l',
												text=type.title(), sub_theme="Menu",
												options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.rframe = bgui.Frame(self.mframe, "right_frame", size=[0.4, 0.8], pos=[0.5, 0.1])
		self.rframe.colors = [[0, 0, 0, 0] for i in range(4)]
		self.pframe = bgui.Frame(self.rframe, "player_frame", size=[1, 0.4], pos=[0, 0.6], sub_theme="Menu")
		self.iframe = bgui.Frame(self.rframe, "item_frame", size=[1, 0.55], pos=[0, 0], sub_theme="Menu")
		
		# Player equipment
		self.weaponlbl = bgui.Label(self.pframe, 'weaponlbl', text="Weapon:", sub_theme="Menu", pos=[0.03, 0.90])
		self.weapon = bgui.Label(self.pframe, 'weapon', sub_theme='Menu', pos=[0.3, 0.90])
		self.shieldlbl = bgui.Label(self.pframe, 'shieldlbl', text="Shield:", sub_theme="Menu", pos=[0.03, 0.83])
		self.shield = bgui.Label(self.pframe, 'shield', sub_theme='Menu', pos=[0.3, 0.83])
		self.armorlbl = bgui.Label(self.pframe, 'armorlbl', text="Armor:", sub_theme="Menu", pos=[0.03, 0.76])
		self.armor = bgui.Label(self.pframe, 'armor', sub_theme='Menu', pos=[0.3, 0.76])
		# Uncomment these when we actually have accessories.
		self.acclbl = bgui.Label(self.pframe, 'acclbl', text="Accessory:", sub_theme="Menu", pos=[0.03, 0.69])
		self.acc = bgui.Label(self.pframe, 'acc', sub_theme='Menu', pos=[0.3, 0.69])
		
		# XXX We need some sort of horizontal rule
		
		# Player stats
		self.hplbl = bgui.Label(self.pframe, 'hplbl', text='HP:', sub_theme='Menu', pos=[0.03, 0.55])
		self.hp = bgui.Label(self.pframe, 'hp', sub_theme='Menu', pos=[0.15, 0.55])
		self.physdlbl = bgui.Label(self.pframe, 'physdlbl', text='Physical Damage:', sub_theme="Menu", pos=[0.03, 0.40])
		self.physd = bgui.Label(self.pframe, 'physd', sub_theme='Menu', pos=[0.4, 0.40])
		self.arcdlbl = bgui.Label(self.pframe, 'arcdlbl', text='Arcane Damage:', sub_theme="Menu", pos=[0.03, 0.33])
		self.arcd = bgui.Label(self.pframe, 'arcd', sub_theme='Menu', pos=[0.4, 0.33])
		self.accylbl = bgui.Label(self.pframe, 'accylbl', text='Accuracy:', sub_theme="Menu", pos=[0.03, 0.26])
		self.accy = bgui.Label(self.pframe, 'accy', sub_theme='Menu', pos=[0.4, 0.26])
		self.physdeflbl = bgui.Label(self.pframe, 'physdeflbl', text='Physical Defense:', sub_theme="Menu", pos=[0.53, 0.40])
		self.physdef = bgui.Label(self.pframe, 'physdef', sub_theme='Menu', pos=[0.91, 0.40])
		self.arcdeflbl = bgui.Label(self.pframe, 'arcdeflbl', text='Arcane Defense:', sub_theme="Menu", pos=[0.53, 0.33])
		self.arcdef = bgui.Label(self.pframe, 'arcdef', sub_theme='Menu', pos=[0.91, 0.33])
		self.reflexlbl = bgui.Label(self.pframe, 'reflexlbl', text='Reflex:', sub_theme="Menu", pos=[0.53, 0.26])
		self.reflex = bgui.Label(self.pframe, 'reflex', sub_theme='Menu', pos=[0.91, 0.26])
		
		# Item stats
		self.itemname = bgui.Label(self.iframe, 'inlbl', sub_theme='Menu', pos=[0.03, 0.95])
		self.type = bgui.Label(self.iframe, 'type', text='Type:', sub_theme='Menu', pos=[0.03, 0.85])
		self.idesc =  bgui.TextBlock(self.iframe, "info", size=[0.9, .3],
										pos=[0.03, 0.2], sub_theme="")
		
		# Not all of these are currently used, but they could be.
#		self.ihplbl = bgui.Label(self.iframe, 'ihplbl', text='HP:', sub_theme='Menu', pos=[0.03, 0.55])
#		self.ihp = bgui.Label(self.iframe, 'ihp', sub_theme='Menu', pos=[0.15, 0.55])
#		self.iphysdlbl = bgui.Label(self.iframe, 'iphysdlbl', text='Physical Damage:', sub_theme="Menu", pos=[0.03, 0.40])
#		self.iphysd = bgui.Label(self.iframe, 'iphysd', sub_theme='Menu', pos=[0.4, 0.40])
#		self.iarcdlbl = bgui.Label(self.iframe, 'iarcdlbl', text='Arcane Damage:', sub_theme="Menu", pos=[0.03, 0.33])
#		self.iarcd = bgui.Label(self.iframe, 'iarcd', sub_theme='Menu', pos=[0.4, 0.33])
#		self.iaccylbl = bgui.Label(self.iframe, 'iaccylbl', text='Accuracy:', sub_theme="Menu", pos=[0.03, 0.26])
#		self.iaccy = bgui.Label(self.iframe, 'iaccy', sub_theme='Menu', pos=[0.4, 0.26])
		self.iphysdeflbl = bgui.Label(self.iframe, 'iphysdeflbl', text='Physical Defense:', sub_theme="Menu", pos=[0.03, 0.76])
		self.iphysical_defense = bgui.Label(self.iframe, 'iphysdef', sub_theme='Menu', pos=[0.4, 0.76])
		self.iarcdeflbl = bgui.Label(self.iframe, 'iarcdeflbl', text='Arcane Defense:', sub_theme="Menu", pos=[0.03, 0.69])
		self.iarcane_defense = bgui.Label(self.iframe, 'iarcdef', sub_theme='Menu', pos=[0.4, 0.69])
		self.ireflexlbl = bgui.Label(self.iframe, 'ireflexlbl', text='Reflex:', sub_theme="Menu", pos=[0.03, 0.62])
		self.ireflex = bgui.Label(self.iframe, 'ireflex', sub_theme='Menu', pos=[0.4, 0.62])
		
		# Item buttons
		self.drop = Button(self.iframe, "drop_btn", text="DROP", 
								on_click=self.drop_click, pos=[0.2,0.03])
		self.equip = Button(self.iframe, "equip_btn", text="EQUIP", 
								on_click=self.equip_click, pos=[0.6,0.03])
		
	def drop_click(self, widget):
		item = self.lbox.selected
		if item:
			self.lbox.items.remove(item)
			self.main['drop_item'] = item
			
		
	def equip_click(self, widget):
		item = self.lbox.selected
		player = self.main['player']

		if item:
			if self.selection == "weapons":
				player.weapon = item
				player.reset_weapon_mesh(self.main['engine'])
			elif self.selection == "armor":
				player.armor = item
				

	def update(self, main):
		self.main = main
		player = main['player']
		
		if self.selection != self.old_selection:
			self.type_buttons[self.selection].colors = [[0,0,0,0]] * 4
			self.type_buttons[self.selection].border = 0
			
			if self.old_selection:
				self.type_buttons[self.old_selection].colors = [[0,0,0,.1]] * 4
				self.type_buttons[self.old_selection].border = 1
			self.old_selection = self.selection
			
			type = ""
			if self.selection == "weapons":
				type = "Weapon"
			elif self.selection == "armor":
				type = "Armor"
			elif self.selection == "acc.":
				type = "Accessory"
			elif self.selection == "misc.":
				type = "Item"
			self.lbox.items = [item for item in player.inventory
								if item.__class__.__name__==type]
			
		# Update player info
		self.weapon.text = player.weapon.name
		self.shield.text = player.shield.name
		self.armor.text = player.armor.name
		
		self.hp.text = "%d/%d" % (player.hp, player.max_hp)
		self.physd.text = str(player.physical_damage)
		self.arcd.text = str(player.arcane_damage)
		self.accy.text = str(player.accuracy)
		self.physdef.text = str(player.physical_defense)
		self.arcdef.text = str(player.arcane_defense)
		self.reflex.text = str(player.reflex)
		
		# Update item info
		if self.lbox.selected:
			for i in self.iframe.children.values(): i.visible = True
			
			item = self.lbox.selected
			self.itemname.text = item.name
			self.type.text = "Type: %s" % item.type.title()
			self.idesc.text = item.description
			
			if self.selection == "armor":
				for i in ("physical_defense", "arcane_defense", "reflex"):
					lbl = getattr(self, "i"+i)
					diff = getattr(item, i) - getattr(player.armor, i)
					lbl.text = "%d (%+d)" % (getattr(item, i), diff)
					
					if diff > 0:
						lbl.color = (0.15, 0.50, 0.16, 0.9)
					elif diff < 0:
						lbl.color = (0.70, 0.19, 0.16, 0.9)
					else:
						lbl.color = lbl.theme['Color']
			else:
				self.iphysdeflbl.visible = False
				self.iphysical_defense.visible = False
				self.iarcdeflbl.visible = False
				self.iarcane_defense.visible = False
				self.ireflexlbl.visible = False
				self.ireflex.visible = False
		else:
			for i in self.iframe.children.values(): i.visible = False
		
	def selection_click(self, widget):
		self.lbox.selected = None
		self.selection = widget.name
		
class PowersLayout(Layout):
	class PowerCell(bgui.ListBoxRenderer):
		def __init__(self, listbox):
			bgui.ListBoxRenderer.__init__(self, listbox)
			self.listbox = listbox
			
			self.frame = bgui.Frame(listbox, "frame", size=[1, 0.0625],
							   sub_theme="Submenu")
			
			self.nframe = bgui.Frame(self.frame, "name_f", size=[.5, 1],
								pos=[0,0], sub_theme="Submenu")
		
			self.dframe = bgui.Frame(self.frame, "del_f", size=[.3, 1],
								pos=[.5,0], sub_theme="Submenu")
		
			self.tframe = bgui.Frame(self.frame, "tier_f", size=[.2, 1],
								pos=[.8,0], sub_theme="Submenu")
		
			self.nlbl = bgui.Label(self.nframe, "name_l",
								pos=[.05,.2],sub_theme="Menu",
								options=bgui.BGUI_DEFAULT)
			
			self.dlbl = bgui.Label(self.dframe, "del_l", sub_theme="Menu", pos=[0,0.2],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			
			self.tlbl = bgui.Label(self.tframe, "tier_l", sub_theme="Menu", pos=[0,0.2],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		def render_item(self, power):
			
			color = [[0,0,0,0]] * 4
			if power == self.listbox.selected:
				color = [[0,0,0,.1]] * 4
				
			self.frame.colors = color
			self.nlbl.text = power.name
			self.dlbl.text = power.delivery.title()
			if hasattr(self, 'affinities'):
				self.tlbl.text = str(power.cost(self.affinities))
			
			# Mark known powers as white
			if hasattr(self, "known_powers"):
				for i in self.known_powers:
					if power.name == i.name:
						power_color = [1, 1, 1, 1]
						break
				else:
					power_color = self.nlbl.theme['Color']
					
				self.nlbl.color = self.dlbl.color = self.tlbl.color = power_color
			
			return self.frame
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "powers_overlay", state, use_mouse=True)
		
		self.mframe = bgui.Image(self, "1x1_frame",
								"Textures/ui/menu_background.png",
								aspect=1, size=[0,.9],
								options=BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.ele_bar = ElementBar(self.mframe)
		
		self.mframe.position = [.675-self.mframe.size[0]/parent.size[0],
								self.mframe.position[1]]

		self.lframe = bgui.Frame(self.mframe, "list_frame", size=[0.545,0.695],
								pos=[0.05,0.05], sub_theme="Menu")
		
		self.hframe = bgui.Frame(self.lframe, "header", size=[1, .0625],
								pos=[0, 0.9375], sub_theme="Menu")
		
		self.nframe = bgui.Frame(self.hframe, "name_f", size=[.5, 1],
								pos=[0,0], sub_theme="Submenu")
		
		self.nlbl = bgui.Label(self.nframe, "name_l", sub_theme="Subtitle",
								pos=[0.05,0], text="NAME OF POWER",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.dframe = bgui.Frame(self.hframe, "del_f", size=[.3, 1],
								pos=[.5,0], sub_theme="Submenu")
		
		self.dlbl = bgui.Label(self.dframe, "del_l", sub_theme="Subtitle",
								pos=[0.05,0], text="DELIVERY",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.tier_frame = bgui.Frame(self.hframe, "tier_f", size=[.2, 1],
									pos=[.8,0], sub_theme="Submenu")
		
		self.tier_lbl = bgui.Label(self.tier_frame, "tier_l",
								pos=[0.05,0], text="COST", sub_theme="Subtitle",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.lbox = bgui.ListBox(self.lframe, "lb", size=[1, .9375])
		
		self.lbox.renderer = self.PowerCell(self.lbox)
		
		self.tframe = bgui.Frame(self.mframe, "title_frame", size=[0.545,0.08],
								pos=[0.05, 0.745], sub_theme="Menu")
		
		self.title = bgui.Label(self.tframe, "title", text="Powers",
								sub_theme="Title", pos=[0.05,0],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.iframe = bgui.Frame(self.mframe, "info", size=[.335,.66],
								pos=[.615, .165], sub_theme="Menu")
		
		self.pframe = bgui.Frame(self.mframe, "points_frame", size=[.115,.115],
									pos=[.615, .05], sub_theme="Menu")
		
		self.pp_text = bgui.Label(self.pframe, "pp_lbl", sub_theme="Title", text="#",
							options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.pow_name = bgui.Label(self.iframe, "name_lbl", sub_theme="Title",
									pos=[.05, .93], text="")
		
		self.pow_sub = bgui.Label(self.iframe, "sub_lbl", sub_theme="Subtitle",
									pos=[.05, .88], text="")
		
		self.pow_info = bgui.TextBlock(self.iframe, "info", size=[0.9, .3],
										pos=[0.05, 0.5], sub_theme="")
		
		self.pow_details = bgui.TextBlock(self.iframe, "details", size=[0.9, 0.3],
											pos=[0.05, 0.2], sub_theme="")
							
		
		self.acc_btn = Button(self.mframe, "accept_btn", type="EMPHASIS",
								text="ACCEPT", pos=[.75, .085],
								on_click=self.accept_click)
		
		self.can_btn = Button(self.mframe, "cancel_btn", text="CANCEL", 
								on_click=self.cancel_click, pos=[0.75,0.035])
		
		self.buy_btn = Button(self.iframe, "buy_btn", text="BUY", on_click=self.buy_click,
								pos=[0, .1], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

		self.sell_btn = Button(self.iframe, "sell_btn", text="SELL", on_click=self.sell_click,
								pos=[0, .1], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		self.init = False
		
	def update(self, main):
		player = main['player']
		
		if not self.init:
			self.main = main
			self.element = ""
			self.ele_bar.timer = 20
			self.ele_bar.element = player.element
			
			self.powers = []
			self.pp = player.power_pool
			
			self.init= True
		
		if self.element != self.ele_bar.element:
			self.element = self.ele_bar.element
			self.powers = [power for power in Power.get_package_list()
							if power.element == self.element.upper()
							and power.tier <= 1]
			self.lbox.items = self.powers
			self.lbox.active = None
				
		self.pp_text.text = str(self.pp)
	
		name = ""
		sub = ""
		info = "Select a power on the left to learn more about it and to purchase it."
		details = ""

		# Kinda hacky, but should be fine
		self.lbox.renderer.known_powers = player.powers.all
		self.lbox.renderer.affinities = player.affinities
		
		self.buy_btn.visible = False
		self.sell_btn.visible = False
		if self.lbox.selected:
			power = self.lbox.selected
			name = power.name
			sub = "Tier %d - %s" % (power.tier, power.element.title())
			info = power.description
			details = "Cost: %d" % power.cost(player.affinities)
			
			for i in player.powers.all:
				if power.name == i.name:
					self.sell_btn.visible = True
					break
			else:
				self.buy_btn.visible = True
			
		self.pow_name.text = name
		self.pow_sub.text = sub
		self.pow_info.text = info
		self.pow_details.text = details
		
	def buy_click(self, widget):
		player = self.main['player']
		cont = self.main['player_controller']
		
		power = self.lbox.selected
		cost = power.cost(player.affinities)
		
		if cost <= self.pp:
			player.powers.add(power, cont)
			self.pp -= cost
			
	def sell_click(self, widget):
		player = self.main['player']
		cont = self.main['player_controller']
		
		power = self.lbox.selected
		cost = power.cost(player.affinities)
		
		self.pp += cost
		
		for i in player.powers.all:
			if i.name == power.name:
				player.powers.remove(i, cont)
				break
			
	def accept_click(self, widget):
		self.main['player_exit'] = True
			
	def cancel_click(self, widget):
		self.cancel()
		self.main['player_exit'] = True
		
	def cancel(self):
		player = self.main['player']
		cont = self.main['player_controller']
		player.powers.remove_all(cont)
		for power in self.main['player_old_powers']:
			player.powers.add(power, cont)
		
class TitleLayout(Layout):
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "title_layout", state, use_mouse=True)
		
		self.bg = bgui.Frame(self, "title_bg", size=[1, 1], pos=[0, 0])
		self.bg.colors = [[0, 0, 0, 1]]*4
		# Background image
		self.img = bgui.Image(self, "title_splash", "Textures/TitleSplash.png",
									size=[0, 1], aspect=1,
									 options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.splash = bgui.Frame(self, "main_frame", size=[1, 1], pos=[0, 0])
		self.splash.colors = [[0, 0, 0, 0]]*4
		
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
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "start_game_overlay", state, use_mouse=True)
		
		# Background frame
		self.frame = bgui.Image(self, "sgo_frame", "Textures/ui/menu_background.png",
								aspect=1, size=[.33, .66], pos=[0.30, 0.05],
			sub_theme='HUD')
		
		ysize = 0.05 # Tweak this to get the inputs and labels to line up
		
		self.userlbl = bgui.Label(self.frame, "sgo_usr_lbl", text="Username: ", pos=[0.05, 0.8])
		self.user = bgui.TextInput(self.frame, "sgo_user",
				size=[0.5, ysize], pos=[0.3, 0.8], text="User")
				
		self.iplbl = bgui.Label(self.frame, "sgo_ip_lbl", text="Server IP: ", pos=[0.05, 0.7])
		self.ip = bgui.TextInput(self.frame, "sgo_ip",
				size=[0.5, ysize], pos=[0.3, 0.7], text="localhost")
				
		self.portlbl = bgui.Label(self.frame, "sgo_port_lbl", text="Server Port: ", pos=[0.05, 0.6])
		self.port = bgui.TextInput(self.frame, "sgo_port",
				size=[0.5, ysize], pos=[0.3, 0.6], text="9999")
		
		self.tabs = [self.user, self.ip, self.port]
		self.tab_idx = 0

		# "Go" button
		self.go_button = Button(self.frame, "sgo_go", text="", pos=[0.75, 0.05])
		self.go_button.on_click = self.button_click
			
	def update(self, main):
		self.main = main
		if not self.go_button.text:
			self.go_button.text = "Start" if main['is_host'] else "Join"
		if main['is_host']:
			if self.ip.visible:
				self.ip.visible = False
				self.iplbl.visible = False
			if self.ip in self.tabs:
				self.tabs.remove(self.ip)
			
			
	def button_click(self, widget):
		self.main['user'] = self.user.text
		self.main['addr'] = (self.ip.text, int(self.port.text))
		self.main['start_game'] = True

	def _handle_key(self, key, is_shifted):
		keys = bgui.key_defs
		
		if key == keys.TABKEY:
			if is_shifted:
				self.tab_idx -= 1
				if self.tab_idx < 0:
					self.tab_idx = len(self.tabs) - 1
			else:
				self.tab_idx = (self.tab_idx + 1) % len(self.tabs)
			for v in self.tabs:
					v.deactivate()
					v.select_none()
			self.tabs[self.tab_idx].activate()
			self.tabs[self.tab_idx].select_all()
		if key in (keys.ENTERKEY, keys.PADENTER):
			self.button_click(self.go_button)
			
		Widget._handle_key(self, key, is_shifted)

class CreditsOverlay(Layout):
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "credits_overlay", state, use_mouse=True)
		
		# Background frame
		self.frame = bgui.Image(self, "co_frame", "Textures/ui/menu_background.png",
								aspect=1,  size=[0.33, 0.66], pos=[0.30, 0.05],
			sub_theme='HUD')
			
		# Credits text pulled from a file
		with open('../credits.txt') as f:
			self.block = bgui.TextBlock(self.frame, "co_block", text=f.read().replace("\t", "    "),
				size=[0.95, 0.65], pos=[0.05, 0.3])
		
		# "Go" button
		self.go_button = Button(self.frame, "sgo_go", text="Done", pos=[0.75, 0.05])
		self.go_button.on_click = self.button_click
		
	def update(self, main):	
		self.main = main
		
	def button_click(self, widget):
		self.main['overlay_done'] = True

class InGameMenuLayout(Layout):
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "ingame_menu", state, use_mouse=True)
		
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
		
class CharSelectLayout(Layout):
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "char_select_layout", state, use_mouse=True)
		
		self.frame = bgui.Image(self, "csl_frame",
								"Textures/ui/char_select_bg.png",
								aspect=5/3, size=[0,.4],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.frame.position=[0.55-self.frame.size[0]/sys.size[0],
							self.frame.position[1]]
		
		self.cont_btn = Button(self.frame, "cont_btn", text="CONTINUE", type="EMPHASIS",
								pos=[.65, .12], on_click=self.continue_click)
		
		self.prev_btn = Button(self.frame, "prev_btn", type="ARROW_LEFT", text="",
								pos=[0.047, .12], on_click=self.prev_click)
		
		self.next_btn = Button(self.frame, "next_btn", type="ARROW_RIGHT", text="",
								pos=[0.557, .12], on_click=self.next_click)
		
		self.new_btn = Button(self.frame, "new_btn", text="NEW",
								pos=[.34, .12], on_click=self.new_click)
		
		self.del_btn = Button(self.frame, "del_btn", text="DELETE",
								pos=[.13, .12], on_click=self.del_click)
		
		self.char_name = bgui.Label(self.frame, "name", pos=[0.1, .8], sub_theme="Title")
		self.subclass = bgui.Label(self.frame, "subclass", pos=[0.1, .7], sub_theme="Subtitle")
		self.level = bgui.Label(self.frame, "level", pos=[0.1, .6], sub_theme="Subtitle")
				
	def update(self, main):
		self.main = main
		if main['csl_char']:
			char = main['csl_char']
			self.char_name.text = char.name
			self.subclass.text = "%s (%s/%s)" % (char.player_class.subclass[char.element], char.player_class.name, char.element.title())
			self.level.text = "Level %d" % char.level
		
	def continue_click(self, widget):
		self.main['csl_continue'] = True
		
	def new_click(self, widget):
		self.main['csl_new'] = True
		
	def del_click(self, widget):
		self.main['cls_del'] = True
		
	def prev_click(self, widget):
		self.main['csl_index'] -= 1
	
	def next_click(self, widget):
		self.main['csl_index'] += 1
		
class CharGenLayout(Layout):
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "char_gen_layout", state, use_mouse=True)
		
		# Setup the main frame
		self.mframe = bgui.Image(self, "1x1_frame",
								"Textures/ui/menu_background.png",
								aspect=1, size=[0,.65],
								options=BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.mframe.position = [.5-self.mframe.size[0]/parent.size[0],
								self.mframe.position[1]]
		
		# Setup the ring selector
		self.selector = RingSelector(self)
		
		# Setup the name input
		self.name_lbl = bgui.Label(self.mframe, "name_l", text="1. Name",
									pos=[0.07, 0.9], sub_theme="Title")
		
		self.name_in = bgui.TextInput(self.mframe, "name_in", pos=[0.28, 0.89],
										size=[0.2, 0.07], text="Hero", color=(0,0,0,.8))
		
		# Setup the display of current choices
		self.race_lbl = bgui.Label(self.mframe, "race_l", text="2. Race",
									pos=[0.07, 0.85], sub_theme="Subtitle")
		self.class_lbl = bgui.Label(self.mframe, "class_l", text="3. Class",
									pos=[0.07, 0.8], sub_theme="Subtitle")
		self.element_lbl = bgui.Label(self.mframe, "element_l", text="4. Element",
									pos=[0.07, 0.75], sub_theme="Subtitle")
		
		self.race = bgui.Label(self.mframe, "race_l2", text="Kat",
									pos=[0.3, 0.85], sub_theme="Subtitle")
		self.class_ = bgui.Label(self.mframe, "class_l2", text="Hunter",
									pos=[0.3, 0.8], sub_theme="Subtitle")
		self.element = bgui.Label(self.mframe, "element_l2", text="Death",
									pos=[0.3, 0.75], sub_theme="Subtitle")
		
		# Setup description of current focus
		self.focus_info = bgui.TextBlock(self.mframe, "finfo", pos=[0.07, 0.35],
										size=[0.86, 0.37])
		self.focus_details = bgui.TextBlock(self.mframe, "fdetail", pos=[0.07, 0.05],
										size=[0.86, 0.37])
		
		# Add on a couple of buttons
		self.fin_btn = Button(self.mframe, "fin_btn", text="FINISH", pos=[0.65, 0.07],
								type="EMPHASIS", on_click=self.finish_click)
		
		self.cancel_btn = Button(self.mframe, "can_btn", text="CANCEL", pos=[0.4, 0.07],
								on_click=self.cancel_click)
		
		self.help_btn = Button(self.mframe, "help_btn", text="HELP", pos=[0.65, 0.8],
								on_click=self.help_click)
	
	def update(self, main):			
		self.main = main
		self.race.text = self.selector.race
		class_ob = Class(self.selector.player_class)
		self.class_.text = "%s/%s" % (class_ob.name, class_ob.subclass[self.selector.element.upper()])
		self.element.text = self.selector.element.title()
		
		self.focus_info.text = "Click on a Race, Class, or Element to select it.\n\nRace currently only controls appearance.\nClass controls your starting delivery affinities. (weapon and spell)\nElement determines your base elemental affinities."
		self.focus_details.text = ""
		
		data = self.main['cgen_data']
		
		data['name'] = self.name_in.text
		
		if 'race' not in data or data['race'].name != self.race.text:
			data['race'] = Race(self.race.text)
		if 'class' not in data or data['class'].name != self.class_.text:
			data['class'] = class_ob
		if 'element' not in data or data['element'] != self.element.text.upper():
			data['element'] = self.element.text.upper()
	
	def finish_click(self, main):
		self.main['cgen_exit'] = True
	
	def cancel_click(self, main):
		self.main['cgen_data'] = {}
		self.main['cgen_exit'] = True
		
	def help_click(self, main):
		self.main['cgen_help'] = True
		
class DunGenLayout(Layout):
	
	def __init__(self, sys, state):
		
		Layout.__init__(self, sys, "dun_gen_layout", state)
		
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
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "default_state_layout", state)
		
		self.combat = False
		
		# Player data frame
		self.pframe = bgui.Frame(self, "ds_pframe", aspect=2.5, size=[0, 0.14], pos=[0, 0], sub_theme="HUD")
		self.player_name = bgui.Label(self.pframe, "ds_name", pt_size=34, pos=[0.05, 0.70])
		self.classlvl = bgui.Label(self.pframe, "ds_classlvl", pt_size=24, pos=[0.05, 0.50])
		
		# HP
		self.hp_text = bgui.Label(self.pframe, "ds_hp", pt_size=20, pos=[0.05, 0.3])
		self.hp_bar = bgui.ProgressBar(self.pframe, "ds_hp_bar", size=[0.90, 0.03], pos=[0.05, 0.25],
									sub_theme='HP')
									
		# EXP
		self.exp_text = bgui.Label(self.pframe, "ds_exp", pt_size=20, pos=[0.05, 0.1])
		self.exp_bar = bgui.ProgressBar(self.pframe, "ds_exp_bar", size=[0.90, 0.03], pos=[0.05, 0.05],
									sub_theme='Exp')
		
		# Net Players
		self.net_ids = []
		self.net_frames = {}
		self.net_names = {}
		self.net_classlvl = {}
		self.net_hp = {}
		
		# Locked message
		# self.lock_msg = bgui.Label(self, "lock_msg", pt_size=42, pos=[0.35, 0.90])	
		
		# Power Bar
		self.power_imgs = []
		self.power_bar_selection=-1
		self.power_frame = bgui.Frame(self, "ds_frame_pow", aspect=5, size=[0,.12], sub_theme="HUD",
								pos=[0,0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
#		self.power_frame = bgui.Image(self, "ds_frame_pow", "Textures/ui/power_bar.png", aspect=5, size=[0,.12],
#										pos=[0,0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		# Target info
		self.target_frame = bgui.Frame(self, "ds_target", aspect=2.5, size=[0, 0.1],
									 pos=[0,.9], sub_theme="HUD", options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.target_name =  bgui.Label(self.target_frame, "ds_name_target", pt_size=28,
										options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.target_name.text = "Target"
		self.target_frame.visible = False
		
		# Map
#		self.mmap_frame = Map(self, "ds_map", aspect=1, size=[0, .25], pos=[0,0])
#		self.mmap_frame.position = [1-self.mmap_frame.size[0]/sys.size[0], 1-self.mmap_frame.size[1]/sys.size[1]]
#		
#		self.fmap_frame = bgui.Frame(self, "ds_fmap", size=[.8, .8], pos=[0,0],
#								sub_theme="HUD", options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
#		self.fmap_frame.visible = False
		
	def update_powerbar(self, main, update_all):
		psys = main['player'].powers
		powers = psys.all
		
		self.power_bar_selection = psys.active_index
		
		# If the images don't need to be updated, then update the bar for cool downs	
		if not update_all:
			for i in range(len(powers)):
				power = powers[i]
				img = self.power_imgs[i]
				lbl = self.power_timers[i]
				y = 15 if i == self.power_bar_selection else 3
				
				x = (img.position[0]-self.power_frame.position[0])/self.power_frame.size[0]
				y = (y-self.power_frame.position[1])/self.power_frame.size[1]
				img.position = [x, y]
				
				if power.timer > 0:
					lbl.text = "%.0f"%(power.timer/60)
					img.color = ELEMENT_COLOR['NEUTRAL']+[0.0]
				else:
					lbl.text = ""
					img.color = ELEMENT_COLOR[powers[i].element]+[1.0]
			return
		
		# Clear the old images
		for i in self.power_imgs:
			self.power_frame._remove_widget(i)
		self.power_imgs = []
		self.power_timers = []
	
		# Create new images
		for i in range(min(8, len(powers))):
			# Background
			bg = "Textures/ui/power_bar_bg.png"
			img = bgui.Image(self.power_frame, "sbg"+str(i), bg, aspect=1,
							 size=[0, .75], pos=[.03+.16*i, .115])
			img.color = ELEMENT_COLOR[powers[i].element]+[1.0]

			# Power icon
			img_name = powers[i].open_image()
			simg = bgui.Image(img, powers[i].name, img_name, size=[1, 1], pos=[0, 0])
			powers[i].close_image()
			
			lbl = bgui.Label(img, "cdl"+str(i), pt_size=20, options=bgui.BGUI_CENTERED)
			
			self.power_imgs.append(img)
			self.power_timers.append(lbl)
		
	def update(self, main):
		player = main['player']
		self.player_name.text = player.name
		self.classlvl.text = "%s\t\t%d" % (player.player_class.subclass[player.element], player.level)
		self.hp_text.text = "HP (%d/%d)" % (player.hp, player.max_hp)
		self.hp_bar._update_position([0.90*min(player.max_hp/100, 1), 0.03], self.hp_bar._base_pos)
		self.hp_bar.percent = player.hp/player.max_hp
		
		self.exp_text.text = "EXP (%d/%d)" % (player.xp, player.next_level)#player.xp+100-(player.xp%100))
		self.exp_bar.percent = (player.xp-player.last_level)/(player.next_level-player.last_level+1)
		
		self.update_powerbar(main, len(self.power_imgs) != len(player.powers.all))
			
		# Net Players
		missing_players = self.net_ids[:]
		for id, nplayer in main['net_players'].items():
			
			# Only display players (not monsters)
			if not isinstance(nplayer, PlayerLogic):
				continue
			
			# The player's stats are already taken care of
			if id == main['player'].id:
				#missing_players.remove(id)
				continue
			
			# If they weren't in the old list, then the player is new
			if id not in self.net_ids:
				self.net_ids.append(id)
				self.net_frames[id] = bgui.Frame(self, "ds_%sframe"%id, aspect=2.5, size=[0, 0.1], pos=[0,.15], sub_theme="HUD")
				self.net_names[id] = bgui.Label(self.net_frames[id], "ds_%sname"%id, pt_size=28, pos=[0.05, 0.65])
				self.net_names[id].text = '%s@%s' % (nplayer.name, id)
				self.net_classlvl[id] = bgui.Label(self.net_frames[id], "ds_%sclass"%id, pt_size=22, pos=[0.05, 0.35])
				self.net_classlvl[id].text = "%s\t\t%d" % (nplayer.player_class.name, nplayer.level)
				self.net_hp[id] = bgui.ProgressBar(self.net_frames[id], "ds_%shp"%id, size=[0.90, 0.03], pos=[0.05, 0.25],
									sub_theme='HP')
#			else:
#				# The player is still around, so make sure their UI stays
#				missing_players.remove(id)
				
			# Update Net player info and the position of the info
			self.net_frames[id].pos = [0, .15+self.net_ids.index(id)*.1]
			self.net_hp[id].size = [0.90*min(nplayer.max_hp/100, 1), 0.03]
			self.net_hp[id].percent = nplayer.hp/nplayer.max_hp
			
#		for id in missing_players:
#			print("Removing", id)
#			self.net_ids.remove(id)
#			# Remove widgets
#			self.net_frames[id].visible = False

		# Target
		if main['player'].targets:
			self.target_frame.visible = True
			self.target_name.text = main['player'].targets[0].name
		else:
			self.target_frame.visible = False

#		# Map
#		self.mmap_frame.im_buf = main['map_data']
#		if not self.combat:
#			self.fmap_frame.visible = main['full_map']
#			self.mmap_frame.visible = not main['full_map']
		
class CombatLayout(DefaultStateLayout):
	def __init__(self, sys, state):
		DefaultStateLayout.__init__(self, sys, state)
		self.combat = True
		
	def update (self, main):
		DefaultStateLayout.update(self, main)
	
class DeadLayout(Layout):
	def __init__(self, sys, state):
		Layout.__init__(self, sys, "dead_state_layout", state)
		
		self.deadlbl = bgui.Label(self, "deadlbl", pt_size=42, text="You have died. :(\nPress Attack to respawn",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		

class ShopLayout(Layout):
	class ItemCellRenderer():
		def __init__(self, listbox):
			self.frame = bgui.Image(listbox, "frame", "Textures/ui/bottom_border.png",
									size=[1, 0.0625])
			self.label = bgui.Label(self.frame, "label", pos=[.05,.2],
								sub_theme="Menu", options=bgui.BGUI_DEFAULT)
			
		def render_item(self, item):
			self.label.text = item.name
			return self.frame
			
	def __init__(self, parent, state):
		Layout.__init__(self, parent, "inventory_overlay", state, use_mouse=True)
		
		self.mframe = bgui.Image(self, "1x1_frame", "Textures/ui/menu_background.png",
								 aspect=1, size=[0,.9],	sub_theme="HUD",
								 options=BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		self.mframe.position = [.675-self.mframe.size[0]/parent.size[0],
								self.mframe.position[1]]
		
		self.lframe = bgui.Frame(self.mframe, "list_frame", size=[0.4, 0.8], 
								pos=[0.05, 0.1], sub_theme="Menu")
		
		self.lbox = bgui.ListBox(self.lframe, "list_box", size=[1, 0.9])
		self.lbox.renderer = self.ItemCellRenderer(self.lbox)
		
		self.type_buttons = {}
		self.type_labels = {}
		self.selection = "weapons"
		self.old_selection = ""
		for i, type in enumerate(["weapons", "armor", "acc.", "misc."]):
			self.type_buttons[type] = bgui.Frame(self.lframe, type, size=[0.25, 0.1],
													pos=[0.25*i, 0.9])
			self.type_buttons[type].colors = [[0,0,0,0.1]] * 4
			self.type_buttons[type].border = 1
			self.type_buttons[type].border_color = [0.55, 0.29, 0.16, 0.7]
			self.type_buttons[type].on_click = self.selection_click
			self.type_labels[type] = bgui.Label(self.type_buttons[type], type+'l',
												text=type.title(), sub_theme="Menu",
												options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.rframe = bgui.Frame(self.mframe, "right_frame", size=[0.4, 0.8], pos=[0.5, 0.1])
		self.rframe.colors = [[0, 0, 0, 0] for i in range(4)]
		self.pframe = bgui.Frame(self.rframe, "player_frame", size=[1, 0.4], pos=[0, 0.6], sub_theme="Menu")
		self.iframe = bgui.Frame(self.rframe, "item_frame", size=[1, 0.55], pos=[0, 0], sub_theme="Menu")
		
		# Player equipment
		self.weaponlbl = bgui.Label(self.pframe, 'weaponlbl', text="Weapon:", sub_theme="Menu", pos=[0.03, 0.90])
		self.weapon = bgui.Label(self.pframe, 'weapon', sub_theme='Menu', pos=[0.3, 0.90])
		self.shieldlbl = bgui.Label(self.pframe, 'shieldlbl', text="Shield:", sub_theme="Menu", pos=[0.03, 0.83])
		self.shield = bgui.Label(self.pframe, 'shield', sub_theme='Menu', pos=[0.3, 0.83])
		self.armorlbl = bgui.Label(self.pframe, 'armorlbl', text="Armor:", sub_theme="Menu", pos=[0.03, 0.76])
		self.armor = bgui.Label(self.pframe, 'armor', sub_theme='Menu', pos=[0.3, 0.76])
		# Uncomment these when we actually have accessories.
		self.acclbl = bgui.Label(self.pframe, 'acclbl', text="Accessory:", sub_theme="Menu", pos=[0.03, 0.69])
		self.acc = bgui.Label(self.pframe, 'acc', sub_theme='Menu', pos=[0.3, 0.69])
		
		# XXX We need some sort of horizontal rule
		
		# Player stats
		self.hplbl = bgui.Label(self.pframe, 'hplbl', text='HP:', sub_theme='Menu', pos=[0.03, 0.55])
		self.hp = bgui.Label(self.pframe, 'hp', sub_theme='Menu', pos=[0.15, 0.55])
		self.physdlbl = bgui.Label(self.pframe, 'physdlbl', text='Physical Damage:', sub_theme="Menu", pos=[0.03, 0.40])
		self.physd = bgui.Label(self.pframe, 'physd', sub_theme='Menu', pos=[0.4, 0.40])
		self.arcdlbl = bgui.Label(self.pframe, 'arcdlbl', text='Arcane Damage:', sub_theme="Menu", pos=[0.03, 0.33])
		self.arcd = bgui.Label(self.pframe, 'arcd', sub_theme='Menu', pos=[0.4, 0.33])
		self.accylbl = bgui.Label(self.pframe, 'accylbl', text='Accuracy:', sub_theme="Menu", pos=[0.03, 0.26])
		self.accy = bgui.Label(self.pframe, 'accy', sub_theme='Menu', pos=[0.4, 0.26])
		self.physdeflbl = bgui.Label(self.pframe, 'physdeflbl', text='Physical Defense:', sub_theme="Menu", pos=[0.53, 0.40])
		self.physdef = bgui.Label(self.pframe, 'physdef', sub_theme='Menu', pos=[0.91, 0.40])
		self.arcdeflbl = bgui.Label(self.pframe, 'arcdeflbl', text='Arcane Defense:', sub_theme="Menu", pos=[0.53, 0.33])
		self.arcdef = bgui.Label(self.pframe, 'arcdef', sub_theme='Menu', pos=[0.91, 0.33])
		self.reflexlbl = bgui.Label(self.pframe, 'reflexlbl', text='Reflex:', sub_theme="Menu", pos=[0.53, 0.26])
		self.reflex = bgui.Label(self.pframe, 'reflex', sub_theme='Menu', pos=[0.91, 0.26])
		
		# Item stats
		self.itemname = bgui.Label(self.iframe, 'inlbl', sub_theme='Menu', pos=[0.03, 0.95])
		self.type = bgui.Label(self.iframe, 'type', text='Type:', sub_theme='Menu', pos=[0.03, 0.85])
		self.idesc =  bgui.TextBlock(self.iframe, "info", size=[0.9, .3],
										pos=[0.05, 0.3], sub_theme="")
		
		# Item buttons
		self.exit = Button(self.iframe, "exit_btn", text="EXIT", 
								on_click=self.exit_click, pos=[0.2,0.03])
		self.buy = Button(self.iframe, "buy_btn", text="BUY", 
								on_click=self.buy_click, pos=[0.6,0.03])
		
	def exit_click(self, widget):
		self.main['shop_exit'] = True
		pass
#		item = self.lbox.selected
#		if item:
#			self.lbox.items.remove(item)
#			self.main['drop_item'] = item
			
		
	def buy_click(self, widget):
		pass
#		item = self.lbox.selected
#		player = self.main['player']
#
#		if item:
#			if self.selection == "weapons":
#				player.weapon = item
#			elif self.selection == "armor":
#				player.armor = item
				

	def update(self, main):
		self.main = main
		player = main['player']
		shopkeeper = main['shop_keeper']
		
		if self.selection != self.old_selection:
			self.type_buttons[self.selection].colors = [[0,0,0,0]] * 4
			self.type_buttons[self.selection].border = 0
			
			if self.old_selection:
				self.type_buttons[self.old_selection].colors = [[0,0,0,.1]] * 4
				self.type_buttons[self.old_selection].border = 1
			self.old_selection = self.selection
			
			type = ""
			if self.selection == "weapons":
				type = "weapons"
			elif self.selection == "armor":
				type = "armors"
			elif self.selection == "acc.":
				type = "items"
			elif self.selection == "misc.":
				type = "items"
			self.lbox.items = [item for item in getattr(shopkeeper, type)]
			
		# Update player info
		self.weapon.text = player.weapon.name
		self.shield.text = player.shield.name
		self.armor.text = player.armor.name
		
		self.hp.text = "%d/%d" % (player.hp, player.max_hp)
		self.physd.text = str(player.physical_damage)
		self.arcd.text = str(player.arcane_damage)
		self.accy.text = str(player.accuracy)
		self.physdef.text = str(player.physical_defense)
		self.arcdef.text = str(player.arcane_defense)
		self.reflex.text = str(player.reflex)
		
		# Update item info
		if self.lbox.selected:
			for i in self.iframe.children.values(): i.visible = True
			
			item = self.lbox.selected
			self.itemname.text = item.name
			self.type.text = "Type: %s" % item.type.title()
			self.idesc.text = item.description
			self.buy.visible = True
		else:
			self.buy.visible = False
		
	def selection_click(self, widget):
		self.selection = widget.name
