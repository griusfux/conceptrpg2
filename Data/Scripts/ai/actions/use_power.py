from cego import *
from cego.actions._action import *

class use_power(action):
	def __call__(self):
		if len(self.args) < 1:
			return
		
		cont = manager.get_controller()
		cont.use_power(self.agent, self.args[0], auto_range=False)