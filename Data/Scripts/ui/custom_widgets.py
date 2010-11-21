# $Id$

from bgui import *

# This file holds widgets custom made for CRPG2

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
			self.packages[i].close_image()
			img.idx = i
			img.on_click = self.package_image
			self.pkg_imgs.append(img)
			