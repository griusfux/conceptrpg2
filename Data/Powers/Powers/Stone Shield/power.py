import Scripts.effects as Effect

def power(self, controller, user):
	targets = controller.get_targets(self, user)
	if targets == []:
		return
	target = targets[0]
	
	controller.animate_spell(user, "cast")
	controller.add_status(user, "Physical Defense", 0.5, 5)