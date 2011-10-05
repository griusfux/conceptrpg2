from cego.transitions._transition import *

class unlocked(transition):	
	def triggered(self):		
		return self.agent.lock <= 0