import Scripts.effects as effects
import random

def power(self, controller, user):
	
	controller.add_status(user, 'Shield', 4, 'ENCOUNTER')
	
	action = controller.main['default_actions']['1h_idle']
	controller.play_animation(user, action, 0.5)
	