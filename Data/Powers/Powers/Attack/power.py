def power(self, controller, user):

	controller.animate_attack(user, "1h Swing")

	for target in user.targets:
		controller.modify_health(target, -10)