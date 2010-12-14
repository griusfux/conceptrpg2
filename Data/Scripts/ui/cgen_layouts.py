import bgui

from .layouts import Layout
from .custom_widgets import *
from Scripts.packages import *

def TEXTURES(path):
	return "Textures/ui/character select/"+path

class CgenLayout(Layout):
	"""Base layout for the character generation screens"""
	def __init__(self, parent, name):
		self.main = None
		self.prev = 'cgen_name'
		self.next = 'cgen_name'
		
		self.new = True
		
		Layout.__init__(self, parent, "cgen_"+name, use_mouse=True)
		
		# Background image
		bgui.Image(self, name+"_bg", TEXTURES("bg_color.png"), size=[1, 1], pos=[0, 0])
		
		# Grid we will place everything on
		self.grid = bgui.Image(self, name+"_grid", TEXTURES("grid.png"), aspect=(4/3), size=[1,1],
					options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		# Title
		self.title = bgui.Label(self.grid, name+"title", text = "", pt_size=40,
								pos = [.05, .92] if name != "name" else [.05, .6],
								options = bgui.BGUI_DEFAULT)
								
		# Back button
		if name != "character":
			self.prev_btn = bgui.FrameButton(self.grid, name+"back_btn", text="Back",
												pt_size=30, size=[0.2, 0.05], pos=[.5, .4])
			self.prev_btn.on_click = self.prev_page
								
		# Next button
		self.next_btn = bgui.FrameButton(self.grid, name+"next_btn", text="Next",
											pt_size=30, size=[0.2, 0.05], pos=[.73, .4])
		self.next_btn.on_click = self.next_page
					
	def update(self, main):
		self.main = main
		
	def prev_page(self, parent):
		self.main['cgen_input'][self.name[5:]] = self.input()
		self.main['next_layout'] = self.prev
		
	def next_page(self, parent):
		self.main['cgen_input'][self.name[5:]] = self.input()
		self.main['next_layout'] = self.next
		
class CgenSelect(CgenLayout):
	"""Character Generation page for selecting the player's race"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "character")		
		# Set the title
		self.title.text = "Who are you?"
		
		# Set the next page
		self.next = 'start'
		self.next_btn.text = "Start!"
		
		# Character selector
		self.selector = PackageSelector(self.grid, "char_selector", Save, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.last_selected = -1
		
		# Display currently selected character's name
		self.label = bgui.Label(self.grid, "char_lbl", text="", pos=[.46, .85],
								pt_size=36, options = bgui.BGUI_DEFAULT)
		self.label.text = self.selector.current_package.name
		
		# Display the currently selected character's image
		img_name = self.selector.current_package.open_image()
		self.image = bgui.Image(self.grid, "char_img", img_name,
								aspect = 0.75, size = [.45, .45], pos = [.12, .4])
		self.selector.current_package.close_image()
								
		# Info text
		self.class_info = bgui.TextBlock(self.grid, "char_info", pt_size=20, size=[0.44, .30],
										pos=[.46, .5], options=bgui.BGUI_DEFAULT)
		self.class_info.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."		
										
		# Set the input for this page
		self.input = lambda: self.selector.current_package
		
	def update(self, main):
		CgenLayout.update(self, main)
	
		self.label.text = self.selector.current_package.name
		if self.last_selected != self.selector.selected:
			img_name = self.selector.current_package.open_image()
			self.image.update_image(img_name)
			self.selector.current_package.close_image()
			self.last_selected = self.selector.selected
			
		if self.selector.current_package.package_name == "&new":
			self.next_btn.text = "Create!"
		else:
			self.next_btn.text = "Start!"
					
class CgenName(CgenLayout):
	"""Character Generation page for setting the character's name"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "name")
		
		# Set the title
		self.title.text = "What is your name?"
		
		# Get the Player's name
		self.name_img = bgui.Image(self.grid, "name_input_img", "Textures/ui/text_input_hover.png",
								pos=[.33, .5], size=[.33, .05])
		self.name_input = bgui.TextInput(self.name_img, "name_input",pos=[.05, 0.3],
									size = [1,.9], text='Hero',
									options = bgui.BGUI_DEFAULT)
		# self.name_input.frame.colors = [(1, 1, 1, .5)]*4
		
		# Set the input for this page
		self.input = lambda : self.name_input.text
		
		# Set the next page
		self.next = 'cgen_race'
		
		# Set teh previous page
		self.prev = 'cgen_select'
		
	def update(self, main):
		CgenLayout.update(self, main)
		
		# Load a previous value if there is one
		if self.new and "name" in self.main['cgen_input']:
			self.name_input.text = self.main['cgen_input']['name']
			self.new = False
		
class CgenRace(CgenLayout):
	"""Character Generation page for selecting the player's race"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "race")		
		# Set the title
		self.title.text = "Who are your people?"
		
		# Set the previous page
		self.prev = 'cgen_name'
		
		# Set the next page
		self.next = 'cgen_class'
		
		# Race selector
		self.selector = PackageSelector(self.grid, "race_selector", Race, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.last_selected = -1
		
		# Display currently selected race's name
		self.label = bgui.Label(self.grid, "race_lbl", text="", pos=[.46, .85],
								pt_size=36, options = bgui.BGUI_DEFAULT)
		self.label.text = self.selector.current_package.name
		
		# Display the currently selected race's image
		img_name = self.selector.current_package.open_image()
		self.image = bgui.Image(self.grid, "race_img", img_name,
								aspect = 0.75, size = [.45, .45], pos = [.12, .4])
		self.selector.current_package.close_image()
								
		# Info text
		self.class_info = bgui.TextBlock(self.grid, "race_info", pt_size=20, size=[0.44, .30],
										pos=[.46, .5], options=bgui.BGUI_DEFAULT)
		self.class_info.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."		
										
		# Set the input for this page
		self.input = lambda: self.selector.current_package
		
	def update(self, main):
		CgenLayout.update(self, main)
		
		# Load a previous value if there is one
		if self.new and "race" in self.main['cgen_input']:
			for i, package in enumerate(self.selector.packages):
				if package.name == self.main['cgen_input']['race'].name:
					self.selector.selected = i
					break
			else:
				print("Previous race selection not found")
				self.selector.selected = 0
			self.new = False
	
		self.label.text = self.selector.current_package.name
		if self.last_selected != self.selector.selected:
			img_name = self.selector.current_package.open_image()
			self.image.update_image(img_name)
			self.selector.current_package.close_image()
			self.last_selected = self.selector.selected
		
class CgenClass(CgenLayout):
	"""Character Generation page for selecting the player's race"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "class")
		
		# Set the title
		self.title.text = "What is your profession?"
		
		# Set the previous page
		self.prev = 'cgen_race'
		
		# Set the next page
		self.next_btn.text = "Finish!"
		self.next = 'end_cgen'
				
		# Class selector
		self.selector = PackageSelector(self.grid, "class_selector", Class, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
										
		# Display currently selected class's name
		self.label = bgui.Label(self.grid, "class_lbl", text="", pos=[.46, .85],
								pt_size=36, options = bgui.BGUI_DEFAULT)
		self.label.text = self.selector.current_package.name
		
		# Display the currently selected race's image
		img_name = self.selector.current_package.open_image()
		self.image = bgui.Image(self.grid, "class_img", img_name,
								aspect = 0.75, size = [.45, .45], pos = [.12, .4])
		self.selector.current_package.close_image()
		
		# Info text
		self.class_info = bgui.TextBlock(self.grid, "class_info", pt_size=20, size=[0.44, .30],
										pos=[.46, .5], options=bgui.BGUI_DEFAULT)
		self.class_info.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."		
		
		# Class selector
		self.selector = PackageSelector(self.grid, "class_selector", Class, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		self.last_selected = -1
		
		# Set the input for this page
		self.input = lambda: self.selector.current_package
		
	def update(self, main):
		CgenLayout.update(self, main)
		
		# Load a previous value if there is one
		if self.new and "class" in self.main['cgen_input']:
			for i, package in enumerate(self.selector.packages):
				if package.name == self.main['cgen_input']['class'].name:
					self.selector.selected = i
					break
			else:
				print("Previous class selection not found")
				self.selector.selected = 0
			self.new = False
	
		self.label.text = self.selector.current_package.name
		if self.last_selected != self.selector.selected:
			img_name = self.selector.current_package.open_image()
			self.image.update_image(img_name)
			self.selector.current_package.close_image()
			self.last_selected = self.selector.selected
