# $Id: inventory.py 416 2011-02-14 06:51:47Z Moguri $

class Inventory:
	"""This class represents a player's inventory and stores items"""
	
	def __init__(self):
		"""Inventory constructor"""
		
		self.items = []
		self.armor = None
		self.weapon = None
		self.credits = 0
		
	def add(self, item):
		"""Add an item to the inventory
		
		item -- the item to add
		
		"""
		
		self.items.append(item)
		
	def remove(self, item):
		"""Remove an item from the inventory
		
		item -- the item to remove
		
		"""
		
		self.items.remove(item)
