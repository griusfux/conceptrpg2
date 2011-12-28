def push(self, controller, user):
	self.amount = int(self.amount)
	user.mods[self.name] += self.amount
	
def pop(self, controller, user):
	user.mods[self.name] -= self.amount