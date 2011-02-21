import Scripts.effects as effects
import random
ROLL = [1, 4]

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	
	
	damage = random.randint(*ROLL) + random.randint(*ROLL)
	if user.level >= 21:
		damage += random.randint(*ROLL) + random.randint(*ROLL)
	damage += user.int_mod
		
	def f_collision(effect, position):
		controller.modify_health(target, -damage)
		
	target = user.targets[0]
	
	effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
	effect.f_collision = f_collision
	controller.add_effect(effect)
	