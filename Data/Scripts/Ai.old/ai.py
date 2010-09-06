import Scripts.Ai.Behaviors as Behaviors

class ai:
	def __init__(self, monster):
		self.monster = monster
	
	def Update(self):
		for behavior in self.monster.behaviors:
			if behavior.do(self.monster.obj):
				break
		