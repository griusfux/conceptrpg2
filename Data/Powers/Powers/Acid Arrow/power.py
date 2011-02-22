import Scripts.effects as effects
import random
ROLL = [1, 8]

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
		
	def f_collision(effect, position):
		damage = random.randint(1, 8) + random.randint(1, 8) + user.int_mod		
		controller.modify_health(target, -damage)
		controller.add_status(target, "Acid", -5, "SAVE")
		
		second_targets = controller.get_targets(user, "BURST", 1, source=position)
		for second_target in second_targets:
			if second_target == target:
				continue
			controller.modify_health(second_target, -(random.randint(1, 8) + user.int_mod))
			controller.add_status(second_target, "Acid", -5, "SAVE")
		
	target = user.targets[0]
	
	effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
	effect.f_collision = f_collision
	controller.add_effect(effect)
	