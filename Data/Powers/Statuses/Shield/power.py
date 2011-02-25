def power(self, controller, user):
	pass
		
def push(self, controller, user):
	controller.modify_stat(user, 'ac', 4)
	
def pop(self, controllers, user):
	controller.modify_stat(user, 'ac', -4)