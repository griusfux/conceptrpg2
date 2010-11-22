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
		self.items = []
		self.display = [[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None],
						[None, None, None]]
		
		# Setup a main frame
		self.main = bgui.Frame(self, "shop_main", size=[1,1], aspect=(4/3),
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.main.colors = [[0, 0, 0, 0],
							[0, 0, 0, 0],
							[0, 0, 0, 0],
							[0, 0, 0, 0],]
		
		# Shop Name
		name_bg = bgui.Frame(self.main, "shop_name_bg", size=[.56, .08], pos=[.025, .875], sub_theme="HUD")
		self.shop_name = bgui.Label(name_bg, "shop_name_text", pt_size=40, pos=[.05,0],
								options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		self.shop_name.text = "It's a trap!!"
		
		# Shop Inventory
		inventory_bg = bgui.Frame(self.main, "shop_inv_bg", size=[.56, .37], pos=[.025, .3], sub_theme="HUD")
		# bgui.Image(inventory_bg, "shop_item", TEXTURES("null_item"),
					# size=[1/3, 0.5],
					# pos=[0, 0.5], aspect=1)
		
		# Character limit on name = 19
		for i in range(6):
			self.display[i][0] = bgui.Image(inventory_bg, "shop_item_"+str(i), TEXTURES("null_item"),
									size=[1/3, 0.5], pos=[(i%3)/3, -0.5*(i//3)+0.5], aspect=1)
			self.display[i][1] = bgui.Label(self.display[i][0], "shop_item_name_"+str(i), text="",
									pt_size=18, pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			self.display[i][0].on_click = self.set_selected
		
		# Item info
		info = bgui.Frame(self.main, "shop_info_bg", size=[.56, .275], pos=[.025, .025], sub_theme="HUD")
		self.item_name = bgui.Label(info, "item_name", pt_size=30, pos=[.05, .8])
		self.cost = bgui.Label(info, "item_cost_disp", text="\t", pt_size=25, pos=[.7, .8])
		self.item_cost = bgui.Label(self.cost, "item_cost", text="", pt_size=20, pos=[1, 0])
		self.item_description = bgui.TextBlock(info, "item_desc", pt_size=20, size=[.8, .5],
												pos=[.2, .2])
												
		self.button = bgui.FrameButton(info, "shop_btn", text="Buy", pt_size=25,
										size=[.15, .15], pos=[.5, .05])
		self.button.visible = False
		self.button.on_click = self.btn_on_click
		
		exit = bgui.FrameButton(info, "shop_exit", text="Exit", pt_size=25, size=[.15, .15], pos=[.7, .05])
		exit.on_click = self.exit_on_click
		
	def btn_on_click(self, widget):
		self.main['shop_purchase'] = self.items[self.selected]
		
	def exit_on_click(self, widget):
		self.main['shop_exit'] = True
		
	def update(self, main):
		self.main = main
		self.shop_name.text = main['shop_keeper'].name
		
		if not self.items:
			shopkeeper = main['shop_keeper']
			self.items = shopkeeper.items + shopkeeper.weapons + shopkeeper.armors
			
		if len(self.items)%6 != 0 or len(self.items) == 0:
			self.items.extend([None]*(6-len(self.items)%6))
			
		if self.update_items:
			for i, item in enumerate(self.items):
				if i > 6:
					break #No support for overflow yet :P
				self.display[i][0].update_image(item.open_image() if item else TEXTURES("null_item"))
				self.display[i][1].text = item.name if item else ""
				self.display[i][2] = item if item else None
			self.update_items = False
		
		# Update selection info
		if self.selected != self.last_selected:
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
		
	def set_selected(self, widget):
		self.selected = int(widget.name[-1])