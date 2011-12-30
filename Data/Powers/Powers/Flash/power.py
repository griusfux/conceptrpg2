import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	
	controller.animate_spell(user, "cast")

	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("flash", pos, ori, 60)
	controller.add_effect(effect)

	for target in targets:
		amount = -1 * self.tier
		controller.add_status(target, "Reflex", amount, 1)
		controller.add_status(target, "Accuracy", amount, 1)