import Scripts.effects as Effect

def power(self, controller, user):	
	controller.animate_spell(user, "cast")

	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("small_smoke_green", user, ori, 50)
	controller.add_effect(effect)
	
	effect = Effect.StaticEffect("small_cloud_green", user, ori, 100, delay=50, continuous=0)
	id = controller.add_effect(effect)

	user.add_callback("poison dagger", "ATTACK", poison_dagger_callback(controller, id))
		
class poison_dagger_callback:
	def __init__(self, controller, id):
		self.time = 3
		self.effect_id = id
		self.controller = controller
		
	def __call__(self, state):
		if state['HIT']:
			self.controller.add_status(state['TARGET'], "Poison", .1, 3)
		self.time -= 1
		if self.time<= 0:
			self.controller.remove_effect(self.effect_id)
		return state, self.time<=0