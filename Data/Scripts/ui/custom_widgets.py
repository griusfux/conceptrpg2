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

# $Id$
import os

from bgui import *
import bge

from Scripts.packages import Race, Class

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
		
class Button(Image):
	def __init__(self, parent, name, pos=[0,0], type="DEFUALT", text="Button",
				on_click=None, resize=True, options=BGUI_DEFAULT):
		
		self.resize = resize
		img_str = "Textures/ui/buttons/default.png"
		text = text
		aspect = 3
		size = [0, 45]
		text_size = 24
		text_color = [0.55, 0.29, 0.16, 0.7]#[143/255, 59/255, 5/255, .75]
		
		if type=="EMPHASIS":
			size[1] = 60
			text_size=28
		elif type == "ARROW_LEFT":
			img_str = "Textures/ui/buttons/arrow_left.png"
			aspect = 1
		elif type == "ARROW_RIGHT":
			img_str = "Textures/ui/buttons/arrow_right.png"
			aspect = 1
		
		size[1] *= parent.system.size[1]/1000
		size[1] /= parent.size[1]
		
		Image.__init__(self, parent, name, img_str, aspect, size, pos, options=options)
		if on_click:
			self.on_click = on_click
		
		self.lbl = Label(self, name+'lbl', text=text, pt_size=text_size,
							color=text_color, options=BGUI_DEFAULT|BGUI_CENTERED)

			
	def _resize(self):
		if not self.resize or self.lbl.size[0] < self.size[0]:
			return
		self.aspect=None
		self.size = [(self.lbl.size[0] *1.5)/self.parent.size[0],
					self.size[1]/self.parent.size[1]]
		self._remove_widget(self.lbl)
		self.lbl = Label(self, name+'lbl', text=text, pt_size=text_size,
							color=text_color, options=BGUI_DEFAULT|BGUI_CENTERED)

	@property
	def text(self):
		return self.lbl.text
	
	@text.setter
	def text(self, value):
		self.lbl.text = value
		self._resize()
						
class ElementBar(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, "ele_bar", 0, None, [.9,.1], [0,.85],
						options=BGUI_DEFAULT|BGUI_CENTERX)
		
		self.colors = [[0,0,0,0]]*4
		
		self._element = "Neutral"
		self.timer = 0
		
		path = "Textures/Elements/"
		elements = ["Death", "Storm", "Fire", "Neutral", "Holy", "Earth", "Water"]
		self.icons = {}
		
		for i, element in enumerate(elements):
			self.icons[element] = Image(self, element, path+element+'.png', aspect=1,
										size=[0, .7], pos=[.0975+.11*i, 0],
										options=BGUI_DEFAULT|BGUI_CENTERY)
			self.icons[element].on_click = self.swap
		
		cur = self.icons[self._element]
		cur.size = [self.size[1]/self.size[0], 1]
		
		offset = (cur.size[0] - self.icons["Earth"].size[0])/self.size[0]/2
		cur.position = [(cur.position[0]-self.position[0])/self.size[0] - offset, 0]
		
	def _draw(self):
		Frame._draw(self)
		self.timer += 1
	
	@property
	def element(self):
		return self._element
	
	@element.setter
	def element(self, value):
		value = value.title()
		
		if value == self._element or self.timer < 10:
			return
		
		self.timer=0
		
		prev = self.icons[self._element]
		cur = self.icons[value]
		
		prev.size = [.7*(self.size[1]/self.size[0]), .7]
		cur.size = 	[self.size[1]/self.size[0], 1]
		
		offset = (cur.size[0] - prev.size[0])/self.size[0]/2
		prev.position = [(prev.position[0]-self.position[0])/self.size[0] + offset, 0]
		cur.position = [(cur.position[0]-self.position[0])/self.size[0] - offset, 0]

		self._element = value
		
	def swap(self, widget):
		self.element = widget.name
		
class AffinityWidget(Frame):
	def __init__(self, parent, size, pos):
		Frame.__init__(self, parent, "aw", size=size, pos=pos)
		self.colors = [[0,0,0,0]]*4

		self.icons = {}
		self.labels = {}
		
		# These will be updated in update()
		self.affinities = None
		self.affinity_points = 0
		self.delivery_points = 0
		
		# Element Affinities
		elements_path = "Textures/Elements/"
		self.elements = elements = ["Death", "Storm", "Fire", "Neutral", "Holy", "Earth", "Water"]
		
		self.elementlbl = Label(self, 'ele_affinities', sub_theme="Menu", pos=[0, 0.95],
							options = BGUI_DEFAULT|BGUI_CENTERX)

		for i, element in enumerate(elements):
			# We play around with i to so we get a second column after the 4th element
			x = 0.10 if i < 4 else 0.50
			if i >= 4:
				i -= 4
			y = 0.95 - ((i+1)*0.14)
			
			icon = self.icons[element] = Image(self, element, elements_path+element+'.png', aspect=1,
										size=[0, .12], pos=[x, y])
			icon.on_click = self.aff_click
			self.labels[element] = Label(self, element+"lbl", sub_theme="Affinity", pos=[x+0.25, y+0.04])
			
		# Delivery Affinities
		deliveries_path = "Textures/Deliveries/"
		self.deliveries = deliveries = ["Weapon", "Spell"]
			
		self.deliverylbl = Label(self, 'del_affinities', sub_theme="Menu", pos=[0, 0.3],
							options = BGUI_DEFAULT|BGUI_CENTERX)
		
		for i, delivery in enumerate(deliveries):
			x = 0.10
			y = 0.3-((i+1)*0.14)
			
			icon = self.icons[delivery] = Image(self, delivery, deliveries_path+delivery+'.png', aspect=1,
										size=[0, .12], pos=[x, y])
			icon.on_click = self.aff_click
			self.labels[delivery] = Label(self, delivery+"lbl", sub_theme="Affinity", pos=[x+0.25, y+0.04])
			
	def update(self, player):
		self.player = player
		
		if self.affinities is None:
			self.affinities = player.affinities.copy()
			self.affinity_points = player.affinity_points
			self.delivery_points = player.delivery_points
		
		self.elementlbl.text = "Elemental [Points %d]" % self.affinity_points
		self.deliverylbl.text = "Delivery [Points %d]" % self.delivery_points
		
		for affinity in self.elements + self.deliveries:
			self.labels[affinity].text = "%3d" % self.affinities[affinity.upper()]
			
	def aff_click(self, widget):
		affinity = widget.name.upper()
		
		if self.affinity_points > 0:
			self.affinity_points -= 1
			self.affinities[affinity] += 1
			
			# Temporarily change the player's affinity
			aff = self.player.affinities.copy()
			self.player.affinities = self.affinities.copy()
			self.player.recalc_stats()
			self.player.affinities = aff
		
class RingSelector(Widget):
	"""A widget to use in the character creation screen"""
	
	def __init__(self, parent):
		Widget.__init__(self, parent, "ring_select", aspect=3/2, size=[0,1], pos=[.5,0])
		self.focus = None
		slots = [[.048, 0.27], [0.05, 0.397], [0.055, 0.545], [.063, 0.69], [.076, 0.84], [0.06, 0.155]]
		elements = ["Death", "Storm", "Fire", "Holy", "Earth", "Water"]
		races = Race.get_package_list()
		classes = Class.get_package_list()
		
		self.classes = []	
		for i, class_ in enumerate(classes):
			self.classes.append(Image(self, "class&*"+class_.name, class_.open_image(),
									aspect=1, size=[0, .065],
									pos=[slots[i][0]+.047+.001*i, slots[i][1]]))
			self.classes[i].on_click = self.click
		
		self.races = []	
		for i, race in enumerate(races):
			self.races.append(Image(self, "race&*"+race.name, race.open_image(),
									aspect=1, size=[0, .065],
									pos=[slots[i][0]+.094+.002*i, slots[i][1]]))
			self.races[i].on_click = self.click
		
		self.elements = []
		for i, element in enumerate(elements):
			self.elements.append(Image(self, "element&*"+element,
										"Textures/Elements/"+element+".png", aspect=1,
										size=[0, .065], pos=slots[i]))
			self.elements[i].on_click = self.click
			
		self.element = self.elements[0].name.split('&*')[1]
		self.race = self.races[0].name.split('&*')[1]
		self.player_class = self.classes[0].name.split('&*')[1]
		
	def click(self, widget):
		self.focus = widget.name.split('&*')
		if self.focus[0] == "element":
			self.element = self.focus[1]
		elif self.focus[0] == "class":
			self.player_class = self.focus[1]
		elif self.focus[0] == "race":
			self.race = self.focus[1]
			
	def hover(self, widget):
		self.focus = widget.name.split('&*')

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
		