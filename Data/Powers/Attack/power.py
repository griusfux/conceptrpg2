def power(self, controller, user):

	action = controller.main['default_actions']['1h_attack']
	controller.play_animation(user, action, 4/3)

	for target in user.targets:
		controller.modify_health(target, -10)