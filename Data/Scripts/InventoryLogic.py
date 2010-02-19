class InventoryLogic:
	
	def __init__(self):
		self.weight = 0
		self.items = []
			
	def CalcWeight(self):
		self.weight = 0
		for item in items:
			self.weight += item.weight
					
	def Add(self, item):
		self.items.append(item)
		
	def Remove(self, item):
		try:
			self.items.remove(item)
		except:
			return false