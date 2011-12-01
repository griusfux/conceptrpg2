def push(self, controller, user):
	user.flags.add('HELD')
	
def pop(self, controller, user):
	user.flags.discard('HELD')