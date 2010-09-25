# $Id$
import collections

class Inventory:
	"""This class represents a player's inventory and stores items"""
	
	def __init__(self):
		"""Inventory constructor"""
		
		self.items = collections.OrderedDict()
		self.armor = None
		self.weapon = None
		self.monies = 0
		
	def add(self, item):
		"""Add an item to the inventory
		
		item -- the item to add
		
		"""
		
		self.items[item] = self.items.get(item, 0) + 1
		
	def remove(self, item):
		"""Remove an item from the inventory
		
		item -- the item to remove
		
		"""
		
		self.items[item] -= 1
		
		if self.items[item] < 1:
			del self.items[item]
