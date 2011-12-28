import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("small_smoke", pos, ori, 50)
	controller.add_effect(effect)
	
	new_pos = target.object.position
	new_pos = new_pos - target.object.forward_vector
	new_pos *= user.weapon.range
	controller.reposition(user, new_pos)
	rotation = user.object.forward_vector.rotation_difference(target.object.forward_vector)
	rotation = rotation.to_euler()
	controller.move(user, angular=rotation)
		
	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("small_smoke", pos, ori, 50)
	controller.add_effect(effect)
	
	controller.attack(self, user, multiplier=2)