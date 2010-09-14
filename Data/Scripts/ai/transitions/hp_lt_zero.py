from Scripts.ai.transitions.transition import transition

class hp_lt_zero(transition):
	def __init__(self, agent, target_state):
		transition.__init__(self, agent, target_state)
		
	def triggered(self):
		return self.agent.hp < 0