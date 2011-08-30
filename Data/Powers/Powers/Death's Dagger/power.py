import random

import Scripts.effects as Effect

def power(self, controller, user):
	if user.stance == self.name:
		user.stance = ""
		user.remove_callback("ATTACK", self.callback)
		del self.callback
		return
	else:
		user.stance = self.name
	
	controller.animate_spell(user, "cast")

	effect = Effect.StaticEffect("small_smoke", user, 50)
	controller.add_effect(effect)
	
	effect = Effect.StaticEffect("small_cloud_purple", user, 100, delay=50, continuous=0)
	id = controller.add_effect(effect)

	self.callback = death_dagger_callback(user, self.name, controller, id)
	user.add_callback("ATTACK", self.callback)
		
class death_dagger_callback:
	def __init__(self, user, name, controller, id):
		self.effect_id = id
		self.controller = controller
		self.user = user
		self.name = name
		
	def __call__(self, target, hit, damage):
		damage += 4 + random.randrange(0, 3)
		return target, hit, damage, True
	
	def __del__(self):
		self.controller.remove_effect(self.effect_id)