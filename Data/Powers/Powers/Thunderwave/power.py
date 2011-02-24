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
	
	source = user.object.position
		
	def f_collision(effect, position):
		if controller.check_save(effect.target, "Fortitude", user, "Intelligence"):
			return
			
		knockback = (effect.target.object.position - source) * user.wis_mod
		controller.move(effect.target, linear=knockback)
		
		controller.modify_health(effect.target, -damage)
	
	for target in user.targets:
		effect = effects.ProjectileEffect("magic_missle", user.object.position, target)
		effect.f_collision = f_collision
		controller.add_effect(effect)
	