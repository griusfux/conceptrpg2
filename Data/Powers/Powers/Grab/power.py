import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	controller.attack(self, user, multiplier=0)
	
	pos = target.object.position
	ori = target.object.get_orientation()
	effect = Effect.StaticEffect("grab", pos, ori, 100)
	controller.add_effect(effect)
	
	controller.add_status(target, "Held", 0, 6)