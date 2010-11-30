import bgui
from .layouts import Layout
from .custom_widgets import *
from Scripts.packages import *

def TEXTURES(path):
	return "Textures/ui/shop/"+path+".png"
	
class ShopLayout(Layout):
	"""Layout for purchasing in game items"""
	def __init__(self, parent):
		Layout.__init__(self, parent, "shop_layout", use_mouse=True)
		self.update_items = True
		self.last_selected = -1
		self.selected = -1
		self.weapons = []
		self.armors = []
		self.misc  = []
		self.items = []
		self.display = [[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None]]
		
		# Setup a main frame
		self.main_frame = bgui.Frame(self, "shop_main", size=[1,1], aspect=(4/3),
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.main_frame.colors = [[0, 0, 0, 0],
							[0, 0, 0, 0],
							[0, 0, 0, 0],
							[0, 0, 0, 0],]
		
		# Shop Name
		name_bg = bgui.Frame(self.main_frame, "shop_name_bg", size=[.56, .13], pos=[.025, .85], sub_theme="HUD")
		self.shop_name = bgui.Label(name_bg, "shop_name_text", pt_size=40, pos=[.05,0],
								options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		self.shop_name.text = "It's a trap!!"
		
		# Category Selector
		cat_bg= bgui.Frame(self.main_frame, "cat_sel_bg", size =[.56, .1], pos=[.025, .7])
		cat_bg.colors = [[0,0,0,0]] * 4
		self.weapon_btn = bgui.Image(cat_bg, "cat_weap", "Textures/ui/hex_tile.png",  size=[1, 1], aspect=1, pos=[0,0])
		self.weapon_btn.on_click = self.weap_sel
		self.weapon_btn.visible = False
		
		self.armor_btn = bgui.Image(cat_bg, "cat_armor", "Textures/ui/hex_tile.png",  size=[1, 1], aspect=1, pos=[.13,0])
		self.armor_btn.on_click = self.armor_sel
		self.armor_btn.visible = False
		
		self.misc_btn = bgui.Image(cat_bg, "cat_misc", "Textures/ui/hex_tile.png",  size=[1, 1], aspect=1, pos=[.26,0])
		self.misc_btn.on_click = self.misc_sel
		self.misc_btn.visible = False
		
		# Shop Inventory
		inventory_bg = bgui.Frame(self.main_frame, "shop_inv_bg", size=[.5, 1/3], pos=[.025, .3],)
		inventory_bg.colors = [[0, 0, 0, 0]] * 4
		# Scrollbar of x size = 0.06
		
		# Character limit on name = 19
		for i in range(6):
			self.display[i][0] = bgui.Image(inventory_bg, "shop_item_"+str(i), TEXTURES("null_item"),
									size=[1/3, 0.5], pos=[(i%3)/3, -0.5*(i//3)+0.5], aspect=1)
			self.display[i][1] = bgui.Label(self.display[i][0], "shop_item_name_"+str(i), text="",
									pt_size=18, pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			self.display[i][0].on_click = self.set_selected
		
		# Item info
		info = bgui.Frame(self.main_frame, "shop_info_bg", size=[.56, .275], pos=[.025, .025], sub_theme="HUD")
		self.item_name = bgui.Label(info, "item_name", pt_size=30, pos=[.05, .8])
		self.cost = bgui.Label(info, "item_cost_disp", text="\t", pt_size=25, pos=[.7, .8])
		self.item_cost = bgui.Label(self.cost, "item_cost", text="", pt_size=20, pos=[1, 0])
		self.item_description = bgui.TextBlock(info, "item_desc", pt_size=20, size=[.8, .5],
												pos=[.2, .2])
												
		self.button = bgui.FrameButton(info, "shop_btn", text="Buy", pt_size=25,
										size=[.15, .15], pos=[.5, .05])
		self.button.visible = False
		self.button.on_click = self.buy_on_click
		
		exit = bgui.FrameButton(info, "shop_exit", text="Exit", pt_size=25, size=[.15, .15], pos=[.7, .05])
		exit.on_click = self.exit_on_click
		
		# Purchase confirmation dialouge box
		self.confirm = bgui.Frame(self, "purchase_confirm", size=[.15, .2], sub_theme="HUD",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.confirm_mess = bgui.Label(self.confirm, "confirm_mess", pt_size=25, pos=[.17, .8], text="Purchase: ")
		self.confirm_item = bgui.Label(self.confirm_mess, "confirm_item", pt_size=25, pos=[0, -1.25])
		self.confirm_cost = bgui.Label(self.confirm_mess, "confrim_cost", pt_size=25, pos=[0, -2.5])
		self.confirm_yes = bgui.FrameButton(self.confirm, "confirm_yes", text="Yes", pt_size=25,
											size=[.3, .2], pos=[.17, .1])
		self.confirm_no = bgui.FrameButton(self.confirm, "confirm_no", text="No", pt_size=25,
											size=[.3, .2], pos=[.57, .1])
		self.confirm.visible = False
		
		self.confirm_yes.on_click = self.purchase
		self.confirm_no.on_click = self.cancel
		
		# Not enough gold dialouge
		self.neg = bgui.Frame(self, "not_enough_gold", size=[.25, .15], sub_theme="HUD",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.neg_mess = bgui.TextBlock(self.neg, "neg_mess", pt_size=25, size=[.8, .55],
								pos=[0, .25], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.neg_cancel = bgui.FrameButton(self.neg, "neg_cancel", pt_size=25, text="Cancel",
								size=[.3, .2], pos=[0, .1], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.neg_mess.text = "You do not have enough gold for that."
		self.neg.visible = False
		
		self.neg_cancel.on_click = self.cancel
		
	def weap_sel(self, widget):
		self.items = self.weapons
		self.update_items = True
		
	def armor_sel(self, widget):
		self.items = self.armors
		self.update_items = True
		
	def misc_sel(self, widget):
		self.items = self.misc
		self.update_items = True
		
	def buy_on_click(self, widget):
		"""Brings up the purchase confirmation dialouge box"""
		# Get item
		item = self.items[self.selected]
		
		# If the item is somehow None, don't continue
		if item == None:
			return
			
		self.main_frame.frozen = True
		
		# Check to see if the player can't afford the item
		if self.main['player'].gold < item.cost:
			self.neg.visible = True
			return
		
		# Display confirmation
		self.confirm_item.text = item.name
		self.confirm_cost.text = "For " + str(item.cost) + "g ?"
		self.confirm.visible = True

		
	def set_selected(self, widget):
		"""On click event to handle selecting an item"""
		self.selected = int(widget.name[-1])
		
	def exit_on_click(self, widget):
		"""On click event for exiting the shop"""
		
		self.main['shop_exit'] = True
		
	def purchase(self, widget):
		"""On click event for purchasing an item"""
		
		item = self.items[self.selected]
		self.main['player'].gold -= item.cost
		self.main['player'].inventory.add(item)
		
		self.confirm.visible = False
		self.main_frame.frozen = False

	def cancel(self, widget):
		"""On click event to return to the shop window"""
		
		self.confirm.visible = False
		self.neg.visible = False
		
		self.main_frame.frozen = False
		
	def update(self, main):
		self.main = main
		self.shop_name.text = main['shop_keeper'].name
		
		# Load the shops items if none are loaded yet
		if not self.items:
			# Create an alias
			shopkeeper = main['shop_keeper']
			
			# Fill the lists
			self.weapons = shopkeeper.weapons
			self.armors = shopkeeper.armors
			self.misc = shopkeeper.items
			
			# Display icons that have items in them
			if self.weapons:
				self.weapon_btn.visible = True
			if self.armors:
				self.armor_btn.visible = True
			if self.misc:
				self.misc_btn.visible = True
			
			# Set a default list
			self.items = self.weapons
		
			self.init = True
			
		# Pad the item list to insure it is always a multiple of 6
		if len(self.items)%6 != 0 or len(self.items) == 0:
			self.items.extend([None]*(6-len(self.items)%6))
		
		# Updates the item display
		if self.update_items:
			for i, item in enumerate(self.items):
				# Ignore anything over 6 for now
				if i > 6:
					break
				
				# Update the display elements, and save the item into a convenient location
				self.display[i][0].update_image(item.open_image() if item else TEXTURES("null_item"))
				self.display[i][1].text = item.name if item else ""
				self.display[i][2] = item if item else None
				
			# The display no longer needs updating since it was just updated
			self.update_items = False
			
			# Make sure we can select a new item
			self.selected = -1
		
		# Update selection info
		if self.selected != self.last_selected or self.selected == -1:
			if self.selected == -1:
				self.selected = 0
			# Save the current selection
			self.last_selected = self.selected
			
			# Create a shorthand for the item
			item = self.items[self.selected]
			
			# Display missing elements if valid item is selected
			self.cost.text = "Cost: " if item else "\t"
			self.button.visible = True if item else False
			
			# Fill in the stats for the item
			self.item_name.text = item.name if item else ""
			self.item_cost.text = str(item.cost) + "g" if item else ""
			self.item_description.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sed orci neque. Cras eget neque lacinia leo sodales suscipit sed." if item else ""
			