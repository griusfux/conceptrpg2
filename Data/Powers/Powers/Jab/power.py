import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	pos = target.object.position
	pos[2] += 1
	effect = Effect.StaticEffect("jab", pos, 20)
	controller.add_effect(effect)
	
	controller.add_status(user, "Accuracy", 0.2, 0)
	controller.attack(self, target)