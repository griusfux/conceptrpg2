def power(self, controller, user):
	pass
		
def push(self, controller, user):

	user.unspent_levels[0].ability_points += 4
	user.unspent_levels[0].feats += 1
	user.unspent_levels[0].at_will_count += 1
	
	for stat in ('fortitude', 'reflex', 'will'):
		controller.modify_stat(user, stat, 1)
	
def pop(self, controller, user):
	print("Kat racial traits unloaded?! >:(")