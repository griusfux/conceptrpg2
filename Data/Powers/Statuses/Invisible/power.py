import Scripts.effects as Effect

def power(self, controller, user):
	pass
		
def push(self, controller, user):
	user.flags.add("INVISIBLE")
	if user.object:
		effect = Effect.FadeEffect(user, 30, -1.0)
		controller.add_effect(effect)
	
def pop(self, controller, user):
	user.flags.discard("INVISIBLE")
	if user.object:
		effect = Effect.FadeEffect(user, 30, 1.0)
		controller.add_effect(effect)