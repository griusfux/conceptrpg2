import Scripts.effects as Effect

def power(self, controller, user):
	if user.stance == "Death's Dagger":
		cb = user.callbacks['ATTACK']["death's dagger"]
		controller.end_effect(cb.effect_id)
		user.remove_callback("death's dagger", "ATTACK")
		user.stance = ""
		return
	
	user.stance = "Death's Dagger"
	
	controller.animate_spell(user, "cast")

	ori = user.object.get_orientation()
	effect = Effect.StaticEffect("small_smoke", user, ori, 50)
	controller.add_effect(effect)
	
	effect = Effect.StaticEffect("small_cloud_purple", user, ori, 100, delay=50, continuous=0)
	id = controller.add_effect(effect)

	callback = death_dagger_callback(user, self.name, controller, id)
	user.add_callback("death's dagger", "ATTACK", callback)
		
class death_dagger_callback:
	def __init__(self, user, name, controller, id):
		self.effect_id = id
		self.controller = controller
		self.user = user
		self.name = name
		
	def __call__(self, state):
		state['TYPE'] = 'ARCANE'
		return state, False