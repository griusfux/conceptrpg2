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
		if name != "name":
			self.next_btn = bgui.FrameButton(self.grid, name+"back_btn", text="Back",
												pt_size=30, size=[0.2, 0.05], pos=[.5, .4])
			self.next_btn.on_click = self.prev_page
								
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
					
class CgenName(CgenLayout):
	"""Character Generation page for setting the character's name"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "name")
		
		# Set the title
		self.title.text = "What is your name?"
		
		# Get the Player's name
		self.name_input = bgui.TextInput(self.grid, "name_input", pos = [.33, .5],
									size = [.33, .033], text='Kupoman',
									options = bgui.BGUI_DEFAULT)
		self.name_input.frame.colors = [(1, 1, 1, .5)]*4
		
		# Set the input for this page
		self.input = lambda : self.name_input.text
		
		# Set the next page
		self.next = 'cgen_race'
		
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
		
		# Display currently selected race's name
		self.label = bgui.Label(self.grid, "race_lbl", text="", pos=[.46, .85],
								pt_size=36, options = bgui.BGUI_DEFAULT)
		self.label.text = "Race Foo"
		
		# Info text
		self.class_info = bgui.TextBlock(self.grid, "class_info", pt_size=20, size=[0.44, .30],
										pos=[.46, .5], options=bgui.BGUI_DEFAULT)
		self.class_info.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."		
				
		# Race selector
		self.selector = PackageSelector(self.grid, "race_selector", Race, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
										
		# Set the input for this page
		self.input = lambda: self.selector.current_package
		
	def update(self, main):
		CgenLayout.update(self, main)
	
		self.label.text = self.selector.current_package.name
		
class CgenClass(CgenLayout):
	"""Character Generation page for selecting the player's race"""
	def __init__(self, parent):
		CgenLayout.__init__(self, parent, "class")
		
		# Set the title
		self.title.text = "What is your profession?"
		
		# Set the previous page
		self.prev = 'cgen_race'
		
		# Set the next page
		self.next_btn.text = "Start!"
		self.next = 'start'
		
		# Display currently selected race's name
		self.label = bgui.Label(self.grid, "class_lbl", text="", pos=[.46, .85],
								pt_size=36, options = bgui.BGUI_DEFAULT)
		self.label.text = "Class Bar"
		
		# Info text
		self.class_info = bgui.TextBlock(self.grid, "class_info", pt_size=20, size=[0.44, .30],
										pos=[.46, .5], options=bgui.BGUI_DEFAULT)
		self.class_info.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."		
		
		# Class selector
		self.selector = PackageSelector(self.grid, "class_selector", Class, size=[0.95, 0.3],
										pos=[0, .05], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		# Set the input for this page
		self.input = lambda: self.selector.current_package
		
	def update(self, main):
		CgenLayout.update(self, main)
	
		self.label.text = self.selector.current_package.name
		
class CharacterCreationLayout(Layout):
	def __init__(self, parent):
		Layout.__init__(self, parent, "char_creation_layout", use_mouse=True)
		
		self.races = []
		self.classes = []
		
		self.race_idx = self.class_idx = 0
		
		bg = bgui.Image(self, "cgen_bg", "Textures/ui/character select/bg_color.png", size=[1, 1], pos=[0, 0])
		grid = bgui.Image(self, "cgen_grid", "Textures/ui/character select/grid.png", aspect=(4/3), size=[1, 1], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		# Name
		
		# self.name_lbl = bgui.Label(self, "name", text="Name", pos=[0, .9], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		# bgui.Label(self, "race_lbl", text="Choose your race", pos=[0, 0.85], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		# Race
		
		# self.race_frame = bgui.Frame(self, "races", size=[1, .33], pos=[0, .50])
		# self.race_frame.colors = [[0, 0, 0, 0] for i in range(4)]
		
		# replace these with images
		# self.race_scroll = [
			# bgui.Image(self.race_frame, "race_scroll_left", "Textures/ui/character select/left_arrow.png", aspect=1, size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			# bgui.Image(self.race_frame, "race_scroll_right", "Textures/ui/character select/right_arrow.png", aspect=1, size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			# bgui.Frame(self.race_frame, "race_scroll_left", size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			# bgui.Frame(self.race_frame, "race_scroll_right", size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			# ]
			
		# self.race_scroll[0].on_click = self.race_left
		# self.race_scroll[1].on_click = self.race_right
		
		# Class
		
		bgui.Label(self, "class_lbl", text="Choose your class", pos=[0, 0.45], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		
		self.class_frame = bgui.Frame(self, "classes", size=[1, .33], pos=[0, .1])
		self.class_frame.colors = [[0, 0, 0, 0] for i in range(4)]
		
		# replace these with images
		self.class_scroll = [
			bgui.Image(self.class_frame, "class_scroll_left", "Textures/ui/character select/left_arrow.png", aspect=1, size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			bgui.Image(self.class_frame, "class_scroll_right", "Textures/ui/character select/right_arrow.png", aspect=1, size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			# bgui.Frame(self.class_frame, "class_scroll_left", size=[.07, .21], pos=[0.06, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY),
			# bgui.Frame(self.class_frame, "class_scroll_right", size=[.07, .21], pos=[0.87, 0], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
			]
			
		self.class_scroll[0].on_click = self.class_left
		self.class_scroll[1].on_click = self.class_right
		
		foo = bgui.TextBlock(self, "foo", pt_size=18, size=[0.55, .6], pos=[.33, .33], options=bgui.BGUI_DEFAULT)
		foo.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum vitae enim in erat porttitor imperdiet. Pellentesque vestibulum, lectus eget consectetur aliquam, ligula enim accumsan mauris, id sollicitudin mauris metus eu purus. Etiam dapibus hendrerit tincidunt. Vestibulum ut urna mi, at tincidunt nunc. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti. Maecenas ac mi nunc. Nullam sed posuere augue. Donec massa lorem, gravida et dictum ut, luctus a lorem. Sed urna risus, sollicitudin ut gravida et, vulputate sit amet massa. Curabitur auctor neque at orci pulvinar commodo. In molestie mattis lectus, ac tincidunt nisi suscipit ac. Nam convallis laoreet cursus. Phasellus pharetra vestibulum odio id consequat."
		
		# Go!
		start_btn = bgui.FrameButton(self, "start_btn", text="Start", pt_size=24, size=[0.1, 0.05], pos=[.85, .05])
		start_btn.on_click = self.start
		
	def update(self, main):
		self.main = main
	
		# if not self.races:
			# self.update_races()
		if not self.classes:
			self.update_classes()

	def update_races(self):		
		if self.race_idx+3 > len(self.main['races']):
			max = len(self.main['races'])
		else:
			max = self.race_idx+3
			
		if self.race_idx < 0:
			self.race_idx = 0

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
		