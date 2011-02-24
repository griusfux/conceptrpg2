import Scripts.effects as effects
import random

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	
	for target in user.targets:
		if controller.check_save(target, "Fortitude", user, "Intelligence"):
			controller.modify_health(target, 0)
			continue
			
		damage = random.randint(1, 8)
		damage += user.int_mod
		
		controller.modify_health(target, -damage)
		controller.add_status(target, 'Fire', -5, 'SAVE')
	