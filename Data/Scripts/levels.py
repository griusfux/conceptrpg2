class UnspentLevel:
	def __init__(self, level, player_class):
	
		############F####
		# Abililty points
		if level == 1:
			self.ability_points = 25
			self.ability_spend = "BUY"
		elif level % 3 == 0:
			self.ability_points = 2
			self.ability_spend = "LIMIT_TWO"
		elif level % 5 == 0:
			self.ability_points = 1
			self.abililty_spend = "ALL"
		else:
			self.ability_points = 0
			self.ability_spend = "NONE"
		
		