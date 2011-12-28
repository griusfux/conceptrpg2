import Scripts.effects as Effect

def power(self, controller, user):
	controller.animate_spell(user)
	
	pos = user.object.position
	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("taunt", pos, ori, 30)
	controller.add_effect(effect)