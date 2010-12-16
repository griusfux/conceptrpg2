def power(self, controller, user):
	pass
		
def push(self, user):

	user.unspent_levels[0].ability_points += 4
	user.unspent_levels[0].feats += 1
	user.unspent_levels[0].at_wills += 1
	
	user.fort_buff += 1
	user.reflex_buff += 1
	user.will_buff += 1
	
def pop(self, user):
	print("Kat racial traits unloaded?! >:(")