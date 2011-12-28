import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	controller.animate_weapon(user, "Cast")
	
	pos = target.object.position
	pos[2] += 1
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("large_cloud_black", pos, ori, 100)
	controller.add_effect(effect)
	
	controller.add_status(target, "Accuracy", -0.2, 2)