import Scripts.effects as Effect

def power(self, controller, user):
	controller.animate_spell(user)
	
	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("stone_shield", pos, ori, 50)
	controller.add_effect(effect)
	
	controller.add_status(user, "Physical Defense", 0.5, 5)