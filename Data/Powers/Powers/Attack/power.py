def power(self, controller, user):

	controller.play_animation(user, "1h Swing", 4/3)

	for target in user.targets:
		controller.modify_health(target, -10)