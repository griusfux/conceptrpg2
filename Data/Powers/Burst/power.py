def power(self, controller, user):
	controller.play_animation(user, "cast", 1.0)

	targets = controller.get_targets(user, self.range_type, self.range_size, mask=1)
	for target in targets:
		controller.modify_health(target, -10)