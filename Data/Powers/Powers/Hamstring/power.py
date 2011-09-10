import random

import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	controller.attack(self, target)
	
	if random.random < 0.45:
		controller.add_status(target, "Speed", -0.1, 3)
		controller.add_status(target, "Reflex", -0.1, 3)