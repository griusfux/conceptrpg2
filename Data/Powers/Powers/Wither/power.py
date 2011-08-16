import random

import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	controller.animate_spell(user, "cast")

	def f_collision(effect):
		strength = 4 + random.randrange(0, 3)
		controller.deal_damage(target, strength*0.1, self.tier, self.element, self.delivery)

	pos = user.object.position
	effect = Effect.ProjectileEffect("wither_effect", pos, target)
	effect.f_collision = f_collision
	controller.add_effect(effect)