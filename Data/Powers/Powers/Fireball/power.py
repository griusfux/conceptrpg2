import Scripts.effects as effects
import random

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
		
	def f_collision(effect, position):
		
		targets = controller.get_targets(user, "BURST", 3, source=target.object.position)
		for starget in targets:
				damage = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + user.int_mod
				if controller.check_save(starget, "Reflex", user, "Intelligence"):
					controller.modify_health(starget, -damage//2)
					continue
				controller.modify_health(starget, -damage)
		

		
	target = user.targets[0]
	
	effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
	effect.f_collision = f_collision
	controller.add_effect(effect)
	