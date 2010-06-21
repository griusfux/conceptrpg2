def power(self, combat_system, user, target):
	target.hp += 15
	user.add_lock(1)
	combat_system.play_animation(user, self.animation)