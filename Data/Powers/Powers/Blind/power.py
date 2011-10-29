import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	controller.animate_weapon(user, "throw")
	controller.add_status(target, "Accuracy", -0.2, 2)