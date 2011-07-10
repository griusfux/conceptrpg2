# $Id$

from bgui import *
import bge

# This file holds widgets custom made for CRPG2

class Map(Image):
	def __init__(self, parent, name, aspect=None, size=[0,0], pos=[0, 0],
				sub_theme='', options=BGUI_DEFAULT):
		Image.__init__(self, parent, name, "Textures/ui/map.png", aspect, size,
						pos, sub_theme=sub_theme, options=options)
		
		self.im_buf = None
		
	def _draw(self):
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		
		# Upload the texture data
		if self.im_buf:
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 512, 512,
						 0,	GL_RGBA, GL_UNSIGNED_BYTE, self.im_buf)
		Image._draw(self)
		
class PackageSelector(Widget):
	"""A widget for handling selection from packages (such as race and class selection)"""
	
	def __init__(self, parent, name, package_cls, aspect=None, size=[0, 0], pos=[0, 0], options=BGUI_DEFAULT):
		"""The PackageSelector constructor
		
		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		package_cls -- the class of the packages to use in the selector
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		
		Widget.__init__(self, parent, name, aspect, size, pos, options)
		
		# The list of packages we'll be using
		self.packages = package_cls.get_package_list()
		
		# The current package index
		self.idx = 0
		self.selected = 0
		
		# Scroll arrows
		self.scroll_arrows = [
				Image(self, "pkg_scroll_left", "Textures/ui/character select/left_arrow.png", aspect=1, size=[.2, .2], pos=[0.06, 0], options=BGUI_DEFAULT|BGUI_CENTERY),
				Image(self, "pkg_scroll_right", "Textures/ui/character select/right_arrow.png", aspect=1, size=[.2, .2], pos=[0.87, 0], options=BGUI_DEFAULT|BGUI_CENTERY)
			]
			
		self.scroll_arrows[0].on_click = self.arrow_left
		self.scroll_arrows[1].on_click = self.arrow_right
		
		# The package images to display, which is updated in the update() method
		self.pkg_imgs = []
		
		# Update the widget
		self.update()
		
	def arrow_left(self, widget):
		"""Left arrow on_click"""
		if self.idx != 0:
			self.idx -= 1
		self.update()
		
	def arrow_right(self, widget):
		"""Right arrow on_click"""
		if len(self.pkg_imgs) != 1:
			self.idx += 1
			self.update()
		
	def package_image(self, widget):
		"""Package image on_click"""
		
		self.selected = widget.idx
		
		
	@property
	def current_package(self):
		"""Returns the currently selected package"""
		
		return self.packages[self.selected]
		
	def update(self):
		# Clamp the index value
		max = min(self.idx+3, len(self.packages))
		
		if self.idx < 0:
			self.idx = 0
		
		# Clear the old images
		for i in self.pkg_imgs:
			self._remove_widget(i)
			
		self.pkg_imgs = []
		
		# Create the new images
		
		for i in range(self.idx, max):
			img_name = self.packages[i].open_image()
			img = Image(self, "pkg_img"+str(i), img_name, aspect=0.75,
						size=[1, .9], pos=[.18+(.25*(i-self.idx)), 0], options=BGUI_DEFAULT|BGUI_CENTERY)
			pkg_lbl = Label(img, "pkg_lbl"+str(i), text=self.packages[i].name,
							pt_size=30, options=BGUI_DEFAULT)
			# Center the label manual, since BGUI_CENTERX makes the text box on the previous page stop working
			pkg_lbl._update_position(pkg_lbl._base_size, [(img.size[0]-pkg_lbl.size[0])/(2*img.size[0]), 0])
			
			self.packages[i].close_image()
			img.idx = i
			img.on_click = self.package_image
			self.pkg_imgs.append(img)
			

class ScrollBar(Widget):
	
	def __init__(self, parent, name, size=[0,1], pos=[0,0], width=20, step=.1,
					layout='VERTICAL', sub_theme='', options=BGUI_DEFAULT):
		
		Widget.__init__(self, parent, name, None, size, pos, sub_theme, options)
		
		# Options
		# width = How wide the ScrollBar is, overrides size if size is 0
		# layout = The orientation of the ScrollBar, options include 'HORIZONTAL' and 'VERTICAL'
		# step = how far to increment the ScrollBar on a scroll event
		
		self._layout = layout
		
		# Allow for an on scroll callback
		self.on_scroll = None
		
		# The ScrollBar starts at the beginning
		self._amount = 0
		
		# Save the step
		self.step = step
		
		# Scale the width setting for the system
		width *= self.system.size[1]/1000
		
		# Adjust the appropriate size if it is 0
		if layout=='VERTICAL':
			if self.size[0] == 0:
				self.size[0] = width
				self.position[0] -= width
		else: # HORIZONTAL
			if self.size[1] == 0:
				self.size[1] = width
		
		# Set up a frame to build this widget on
		main_frame = Frame(self, 'scroll_main_frame', size=[1,1], pos=[0,0])
		# self.on_click = self.scroll_up
		main_frame.colors = [[0, 0, 0, 0],] * 4
		
		# Find the size of the arrows (They are 1:1), and their locations
		arrow_size = []
		a1_pos = []
		a2_pos = []
		if layout=='VERTICAL':
			arrow_size = [1, self.size[0]/self.size[1]]
			a1_pos = [0, 1-arrow_size[1]]
			a2_pos = [0, 0]
		else: # HORIZONTAL
			arrow_size = [self.size[1]/self.size[0], 1]
			a1_pos = [0,0]
			a2_pos = [1-arrow_size[0], 0]
			

		# Create the scroll arrow frames (need to pass in copies because they get altered
		up_arrow = Frame(main_frame, 'scroll_up', border=1, size=arrow_size[:], pos=a1_pos)
		up_arrow.on_click = self.scroll_up
		down_arrow = Frame(main_frame, 'scroll_down', border=1, size=arrow_size[:], pos=a2_pos)
		down_arrow.on_click = self.scroll_down
		
		# Create the scroll bar
		bar_size = [1, 1-2*arrow_size[1]] if layout=='VERTICAL' else [1-2*arrow_size[0], 1]
		bar_pos = [0, arrow_size[1]] if layout=='VERTICAL' else [arrow_size[0], 0]
		self._scroll_bar = Frame(main_frame, 'scroll_bar', size=bar_size, pos=bar_pos)
		self._scroll_bar.colors = [[0,0,0,0],]*4
		
		# Create the indicator
		bar_size = [1, self._scroll_bar.size[0]/self._scroll_bar.size[1]] if layout=='VERTICAL' else [self._scroll_bar.size[1]/self._scroll_bar.size[0], 1]
		mark_pos = [0, 1-bar_size[1]] if layout=='VERTICAL' else [0,0]
		self._marker = Frame(self._scroll_bar, 'scroll_marker', border=1, size=bar_size, pos=mark_pos)
		
	def scroll_up(self, widget):
		self.amount -= self.step
	
	def scroll_down(self, widget):
		self.amount += self.step
		
	@property
	def amount(self):
		return self._amount
		
	@amount.setter
	def amount(self, value):
		
		# Ensure 0 <= amount < 1=
		if value < 0:
			value = 0
		elif value > 1:
			value = 1
		
		# Take care of the call back if it is setup
		if self.on_scroll:
			self.on_scroll(self, value-self._amount)
			
		self._amount = value
			
		# Update the marker
		if self._layout == 'VERTICAL':
			pos = (self._scroll_bar.size[1] - self._marker.size[1]) / self._scroll_bar.size[1]
			self._marker.position = [0, (1-self._amount)*pos]
		else: # HORIZONTAL
			pos = (self._scroll_bar.size[0] - self._marker.size[0]) / self._scroll_bar.size[0]
			self._marker.position = [(self._amount)*pos, 0]

class ListBox(Frame):

	def __init__(self, parent, name, list=[], border=1, aspect=None, size=[1, 1],
				pos=[0,0], spacing=15, padding=15, sub_theme='', options=BGUI_DEFAULT):
				
		Frame.__init__(self, parent, 'main_frame', border, aspect, size, pos, sub_theme, options)
		self.colors = [[0,0,0,0],] * 4
		
		self._list_frame = Frame(self, 'list_frame', border=None, size=[1,1], pos=[0,0])
		self._list_frame.colors = [[0,0,0,0],] * 4
		
		self._scroll_bar = ScrollBar(self._list_frame, 'scroll_bar', size=[0.05,1], pos=[.95,0])
		self._scroll_bar.on_scroll = self._scroll
		self._scroll_bar.visible = False
		
		self.spacing = spacing * (self.system.size[1]/1000)
		self.padding = padding * (self.system.size[1]/1000)
		
		self.list = list
		
	@property
	def list(self):
		return self._list
		
	@list.setter
	def list(self, value):
		self._list = []
		previous_size = 0
		
		if not value:
			self._list_size = 0
			self._scroll_bar.step = 0
			return
			
		for item in value:
			if not isinstance(item, Widget):
				print("WARNING: ListBox items must be widgets")
				continue
				
			self._list.append(item)
			previous_size = sum([item.size[1]+self.spacing for item in self._list])
			x = self._list_frame.position[0]
			y = self._list_frame.position[1]+self._list_frame.size[1] - previous_size
			x += self.padding
			x /= self.system.size[0]
			y /= self.system.size[1]
			item.position = [x, y]
			
		self._list_size = previous_size
			
		step = 1 / ((self._list_size+self.padding-self._list_frame.size[1])/self._list_frame.size[1]*len(self._list))
		self._scroll_bar.step = step
		
		
	def _scroll(self, widget, amount):
		amount = amount * ((self._list_size+self.padding-self._list_frame.size[1])/self.system.size[1])
		for item in self._list:
			item.position = [item.position[0]/self.system.size[0], item.position[1]/self.system.size[1] + amount]
		
	def _draw(self):
		Frame._draw(self)
	
		if self._list_size > self._list_frame.size[1]:
			self._scroll_bar.visible = True
			self._scroll_bar._draw()
		
		for item in self._list:
			if item.position[1] < self._list_frame.position[1] or item.position[1]+item.size[1] > self._list_frame.position[1]+self._list_frame.size[1]:
				item.visible = False
			else:
				item.visible = True
		