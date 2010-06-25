from Scripts.item_data import ItemData

class Inventory:
	"""A logic object that stores item data objects"""
	
	def __init__(self):
		self.contents = []
		
	def __call__(self):
		return self.contents