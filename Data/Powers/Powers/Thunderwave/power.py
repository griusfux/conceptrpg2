import random
ROLL = [1, 6]

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	
	
	damage = random.randint(*ROLL)
	if user.level >= 21:
		damage += random.randint(*ROLL)
	damage += user.int_mod
		
	def f_collision(effect):
		effect.endObject()
		target.hp -= damage
	
	for target in user.targets:
		controller.create_effect("magic_missle", user.object._sockets['right_hand'].worldPosition.copy(), target=target.object.gameobj, collision = f_collision)
	
	