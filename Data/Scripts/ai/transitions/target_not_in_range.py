from Scripts.ai.transitions.transition import transition

class target_not_in_range(transition):
	def __init__(self, agent, target_state):
		transition.__init__(self, agent, target_state)
		
	def triggered(self):
		return (self.agent.target.object.position - self.agent.object.position).length > 2