import Scripts.packages as packages

class UnspentLevel:
	def __init__(self, level):
	
		self.ap = 1
		self.pp = 1
		sefl.dp = 0
		self.apply_affinities = False
		
		if level == 1:
			self.ap = 0
			self.pp = 3
			sefl.apply_affiniies = True
		elif level % 5 == 0:
			self.apply_affinities = True
			self.dp = 1
			
		self.level = level
		
		