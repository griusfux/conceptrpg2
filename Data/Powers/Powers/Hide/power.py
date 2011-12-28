import Scripts.effects as Effect

def power(self, controller, user):
	controller.animate_spell(user, "cast")
	
	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("small_smoke", pos, ori, 50)
	controller.add_effect(effect)
	
	controller.add_status(user, "Invisible", 0, 2)