import random
import Scripts.effects as effects

def power(self, controller, user):
	
	if not user.targets:
		return
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	
	
	damage = random.randint(1, 6)
	if user.level >= 21:
		damage += random.randint(1, 6)
	damage += user.int_mod
		
	def f_collision(effect_obj, position):
		controller.modify_health(effect_obj.target, -damage)
	
	for target in user.targets:
		effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
		effect.f_collision = f_collision
		controller.add_effect(effect)
	