def power(self, controller, user):

	action = controller.main['default_actions']['1h_attack']
	controller.play_animation(user, action, 1.0)

	targets = controller.get_targets(user, self.range_type, self.range_size)
	for target in targets:
		controller.modify_health(target, -10)