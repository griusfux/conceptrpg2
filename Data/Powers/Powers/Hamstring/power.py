import random

import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	controller.attack(self, user)
	
	pos = target.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("blood_spread", pos, ori, 50)
	controller.add_effect(effect)
	
	if random.random() < 0.45:
		controller.add_status(target, "Speed", -0.1, 3)
		controller.add_status(target, "Reflex", -0.1, 3)