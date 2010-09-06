import random

class helloworld:	
	def do(obj):
		random.seed()
		if random.choice(range(300)) == 0:
			print("Hello, World!")
			obj.applyForce([0.0, 0.0, 300.0], 1)
			return True
		return False