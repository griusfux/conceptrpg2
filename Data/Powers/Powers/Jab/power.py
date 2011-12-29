import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	pos = target.object.position
	pos[2] += 1
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("jab", pos, ori, 20)
	controller.add_effect(effect)
	
	user.mods['Accuracy'] += user.accuracy*0.2
	user.recalc_stats()
	
	controller.attack(self, user)
	
	user.mods['Accuracy'] -= user.accuracy*0.2
	user.recalc_stats()