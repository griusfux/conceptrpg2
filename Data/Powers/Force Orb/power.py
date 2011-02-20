import Scripts.effects as effects
import random
ROLL = [1, 8]
ROLL2 = [1, 10]

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	
	
	damage = random.randint(*ROLL) + random.randint(*ROLL)
	damage += user.int_mod
		
	def f_collision(effect, position):
		target.hp -= damage
		second_targets = controller.get_targets(user, "BURST", 1, source=position)
		for second_target in second_targets:
			second_target.hp -= random.randint(*ROLL2) + user.int_mod
		
	target = user.targets[0]
	
	effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
	effect.f_collision = f_collision
	controller.add_effect(effect)
	