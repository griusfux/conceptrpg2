from cego.transitions._transition import *

class target_invisible(transition):	
	def triggered(self):
		return "INVISIBLE" in self.agent.targets[0].flags