import Scripts.effects as Effect

def power(self, controller, user):
	controller.animate_spell(user)
	
	pos = user.object.position
	effect = Effect.StaticEffect("taunt", pos, 30)
	controller.add_effect(effect)